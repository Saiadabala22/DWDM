"""SQLite data-warehouse access (replaces the former MySQL setup).

The database is a single file, so no server, user or password is needed.
Location: <project>/data/dwdm_warehouse.db  (override with SQLITE_PATH in .env)
"""
import os
import re
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
SCHEMA = Path(__file__).with_name("schema.sql")
INTERNAL_TABLES = ("etl_runs", "warehouse_metadata")


def db_path() -> Path:
    p = Path(os.getenv("SQLITE_PATH", "data/dwdm_warehouse.db"))
    if not p.is_absolute():
        p = ROOT / p
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


_ENGINES: dict = {}


def get_engine():
    """Return a cached engine for the current database file.

    Streamlit runs scripts on worker threads, so check_same_thread is disabled.
    If the .db file was deleted/moved while the app was running, the engine is
    rebuilt and the schema re-created instead of failing with "no such table".
    """
    path = db_path()
    engine = _ENGINES.get(path)
    if engine is None or not path.exists():
        if engine is not None:
            engine.dispose()
        engine = create_engine(f"sqlite:///{path.as_posix()}", future=True, pool_pre_ping=True,
                               connect_args={"check_same_thread": False})
        init_db(engine)
        _ENGINES[path] = engine
    return engine


def init_db(engine=None):
    engine = engine or get_engine()
    statements = [s.strip() for s in SCHEMA.read_text(encoding="utf-8").split(";") if s.strip()]
    with engine.begin() as c:
        for s in statements:
            c.execute(text(s))


def test_connection() -> bool:
    with get_engine().connect() as c:
        c.execute(text("SELECT 1"))
    return True


def safe_table_name(name: str, default: str = "warehouse_data") -> str:
    name = re.sub(r"\W+", "_", (name or "").strip()).strip("_").lower()
    if not name:
        return default
    if name[0].isdigit():
        name = "t_" + name
    if name in INTERNAL_TABLES:
        raise ValueError(f"'{name}' is reserved for warehouse bookkeeping.")
    return name


def list_tables():
    return sorted(inspect(get_engine()).get_table_names())


def list_data_tables():
    """User/warehouse tables only (internal bookkeeping tables and SQLite internals hidden)."""
    return [t for t in list_tables() if t not in INTERNAL_TABLES and not t.startswith("sqlite_")]


def resolve_table(name: str) -> str:
    """Map a requested table name to the real table name stored in the database.

    Tries an exact match, then a case-insensitive match, then the sanitised
    name used by ETL. Raises ValueError if the table does not exist.
    """
    tables = list_tables()
    if name in tables:
        return name
    low = {t.lower(): t for t in tables}
    if (name or "").lower() in low:
        return low[name.lower()]
    try:
        safe = safe_table_name(name)
    except ValueError:
        safe = None
    if safe and safe in low:
        return low[safe]
    raise ValueError(f"Table '{name}' was not found in {db_path().name}.")


def _quote(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def table_row_count(name: str) -> int:
    t = resolve_table(name)
    with get_engine().connect() as c:
        return int(c.execute(text(f"SELECT COUNT(*) FROM {_quote(t)}")).scalar() or 0)


def db_signature() -> float:
    """Changes whenever the database file is written (used to invalidate cached reads)."""
    p = db_path()
    return p.stat().st_mtime if p.exists() else 0.0


def read_table(name: str, limit: int | None = None) -> pd.DataFrame:
    q = f"SELECT * FROM {_quote(resolve_table(name))}"
    if limit:
        q += f" LIMIT {int(limit)}"
    return pd.read_sql_query(q, get_engine())


def log_etl(dataset_name, table, extracted, transformed, loaded, df):
    with get_engine().begin() as c:
        c.execute(text("INSERT INTO etl_runs (dataset_name,target_table,extracted_rows,transformed_rows,loaded_rows) "
                       "VALUES (:d,:t,:e,:tr,:l)"), dict(d=dataset_name, t=table, e=extracted, tr=transformed, l=loaded))
        c.execute(text("DELETE FROM warehouse_metadata WHERE table_name=:t"), dict(t=table))
        for col, dt in df.dtypes.items():
            c.execute(text("INSERT INTO warehouse_metadata (dataset_name,table_name,column_name,data_type) VALUES (:d,:t,:c,:y)"),
                      dict(d=dataset_name, t=table, c=str(col), y=str(dt)))

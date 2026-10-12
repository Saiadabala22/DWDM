from backend.preprocessing.preprocessing import clean
from backend.database.database import get_engine, safe_table_name, log_etl


def run(df, engine=None, table="warehouse_data", dataset_name="dataset"):
    """Extract -> Transform -> Load into the SQLite warehouse.

    The transform keeps columns readable (no one-hot encoding) so OLAP and
    visualisation work on the stored table; mining modules encode internally.
    """
    engine = engine or get_engine()
    table = safe_table_name(table)
    ex = df.copy()
    tr, info = clean(df, encode=False)
    tr.to_sql(table, engine, if_exists="replace", index=False)
    log_etl(dataset_name, table, len(ex), len(tr), len(tr), tr)
    info["table"] = table
    return ex, tr, info

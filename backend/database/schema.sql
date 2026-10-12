-- SQLite schema for the DWDM warehouse (created automatically on first use)
CREATE TABLE IF NOT EXISTS etl_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_name TEXT,
    target_table TEXT,
    extracted_rows INTEGER,
    transformed_rows INTEGER,
    loaded_rows INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS warehouse_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_name TEXT,
    table_name TEXT,
    column_name TEXT,
    data_type TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

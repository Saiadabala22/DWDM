from utils.ui import load_css
load_css()

import streamlit as st
from backend.etl.etl import run
from backend.database.database import get_engine,db_path
st.title('3. ETL')
df=st.session_state.get('raw_df')
if df is None:st.warning('Upload a dataset first.');st.stop()
table=st.text_input('Warehouse table','warehouse_data')
if st.button('Extract → Transform → Load',type='primary'):
    try:
        ex,tr,info=run(df,get_engine(),table,st.session_state.get('dataset_name','dataset'));st.session_state.processed_df=tr;st.session_state.last_etl_table=info['table'];st.write(info);st.dataframe(tr.head(20),width='stretch');st.success(f"Loaded {len(tr)} rows into SQLite table '{info['table']}' ({db_path().name}).")
    except Exception as e:st.error(f'SQLite/ETL error: {e}')

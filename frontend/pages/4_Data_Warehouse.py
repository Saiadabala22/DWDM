from utils.ui import load_css
load_css()

import streamlit as st
from backend.database.database import test_connection,list_tables,read_table,db_path,INTERNAL_TABLES
st.title('4. Data Warehouse')
st.caption(f'SQLite database file: {db_path()}')
if st.button('Test SQLite connection'):
    try:test_connection();st.success('SQLite connection successful.')
    except Exception as e:st.error(str(e))
try:
    tables=list_tables();data=[t for t in tables if t not in INTERNAL_TABLES]
    if not data:st.info('No warehouse tables yet. Run ETL first.')
    for t in data:
        df=read_table(t,10);st.subheader(t);st.dataframe(df,width='stretch')
    with st.expander('ETL run log & column metadata'):
        for t in INTERNAL_TABLES:
            if t in tables:st.write(t);st.dataframe(read_table(t),width='stretch')
except Exception as e:st.error(f'Database error: {e}')
st.markdown('**Star Schema:** fact table + dimensions.  \n**Snowflake:** normalized dimensions.  \n**Fact Constellation:** multiple fact tables sharing dimensions.')

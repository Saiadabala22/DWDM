from utils.ui import load_css
load_css()

import streamlit as st
from backend.data_input.data_loader import load_dataset,summary
st.title('1. Dataset Upload & Analysis')
f=st.file_uploader('Upload CSV, XLS/XLSX, ARFF or ZIP',type=['csv','xls','xlsx','arff','zip'])
if f:
    try:
        df=load_dataset(f);st.session_state.raw_df=df;st.session_state.dataset_name=f.name
        for c,(k,v) in zip(st.columns(4),summary(df).items()):c.metric(k,v)
        st.dataframe(df.head(25),width='stretch');st.subheader('Statistics');st.dataframe(df.describe(include='all').T,width='stretch')
    except Exception as e:st.error(str(e))

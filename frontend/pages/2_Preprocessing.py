from utils.ui import load_css
load_css()

import streamlit as st
from backend.preprocessing.preprocessing import clean
st.title('2. Data Preprocessing')
df=st.session_state.get('raw_df')
if df is None:st.warning('Upload a dataset first.');st.stop()
enc=st.checkbox('Encode categorical (one-hot)',False,help='Mining pages encode automatically, so this is optional. Encoded data has no text columns left for bar/pie charts.')
sc=st.checkbox('Scale numerical',False)
dup=st.checkbox('Remove duplicates',True)
if st.button('Run Preprocessing',type='primary'):
    x,info=clean(df,enc,sc,dup);st.session_state.processed_df=x;st.json(info);st.dataframe(x.head(25),width='stretch')

from utils.ui import load_css
load_css()

import streamlit as st
from backend.olap.olap import slice_df,dice,rollup,pivot
st.title('5. OLAP')
df=st.session_state.get('processed_df',st.session_state.get('raw_df'))
if df is None:st.warning('Upload/process data first.');st.stop()
num=df.select_dtypes('number').columns.tolist();cat=df.select_dtypes(exclude='number').columns.tolist()
t1,t2,t3,t4=st.tabs(['Slice','Dice','Roll-up / Drill-down','Pivot'])
with t1:
 c=st.selectbox('Dimension',df.columns);v=st.selectbox('Value',df[c].dropna().astype(str).unique());st.dataframe(slice_df(df,c,v),width='stretch')
with t2:
 fs={};
 for c in cat[:3]:
  v=st.multiselect(c,df[c].dropna().astype(str).unique());
  if v:fs[c]=v
 st.dataframe(dice(df,fs),width='stretch')
with t3:
 if num and cat:
  h=st.multiselect('Hierarchy',cat);m=st.selectbox('Measure',num,key='ru_m')
  if h:st.dataframe(rollup(df,h,m),width='stretch')
with t4:
 if len(cat)>=2 and num:
  i=st.selectbox('Index',cat);c=st.selectbox('Columns',[x for x in cat if x!=i]);m=st.selectbox('Measure',num,key='pv_m');st.dataframe(pivot(df,i,c,m),width='stretch')

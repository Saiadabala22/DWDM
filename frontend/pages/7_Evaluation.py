from utils.ui import load_css
load_css()

import streamlit as st,pandas as pd
st.title('7. Evaluation Dashboard')
r=st.session_state.get('classification')
if not r:st.info('Run a classification algorithm first.');st.stop()
m=r['metrics'];st.dataframe(pd.DataFrame([{k:m.get(k) for k in ['Accuracy','Precision','Recall','F1','Kappa','AUC']}]))
st.dataframe(pd.DataFrame(m['Confusion Matrix'],index=r['classes'],columns=r['classes']))

from utils.ui import load_css
load_css()

import streamlit as st,pandas as pd,json
from backend.final_report.report import pdf_bytes,html_bytes,excel_bytes
st.title('9. Final Report & Export')
df=st.session_state.get('processed_df',st.session_state.get('raw_df'))
if df is None:st.warning('Upload data first.');st.stop()
r=st.session_state.get('classification');m=r['metrics'] if r else {}
sections=[('Dataset',f'Rows: {len(df)}\nColumns: {len(df.columns)}\nMissing: {int(df.isna().sum().sum())}'),('Classification',json.dumps({k:m.get(k) for k in ['Accuracy','Precision','Recall','F1','Kappa','AUC']},default=str,indent=2))]
st.download_button('Download PDF',pdf_bytes('Integrated DWDM System Report',sections),'DWDM_Report.pdf','application/pdf')
st.download_button('Download HTML',html_bytes('Integrated DWDM System Report',sections),'DWDM_Report.html','text/html')
st.download_button('Download Excel',excel_bytes({'Dataset':df,'Metrics':pd.DataFrame([{k:m.get(k) for k in ['Accuracy','Precision','Recall','F1','Kappa','AUC']}])}), 'DWDM_Report.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
st.download_button('Download CSV',df.to_csv(index=False),'Processed_Dataset.csv','text/csv')
st.download_button('Download JSON',df.to_json(orient='records',indent=2),'Processed_Dataset.json','application/json')

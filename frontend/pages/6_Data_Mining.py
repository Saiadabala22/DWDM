from utils.ui import load_css
load_css()

import streamlit as st,pandas as pd
from backend.classification.models import run
from backend.association_mining.rules import mine
from backend.clustering.kmeans import run as kmrun,elbow
from backend.visualization.charts import cluster_scatter,elbow_chart,confusion_heatmap
from utils.ui import show_tree
st.title('6. Data Mining')
df=st.session_state.get('processed_df',st.session_state.get('raw_df'))
if df is None:st.warning('Upload data first.');st.stop()
t1,t2,t3=st.tabs(['Classification','Association','Clustering'])
with t1:
 target=st.selectbox('Target',df.columns);alg=st.selectbox('Algorithm',['ID3','J48','Naïve Bayes','k-NN','Random Forest'])
 if st.button('Run Classification',type='primary'):
  try:st.session_state.classification=run(df,target,alg)
  except Exception as e:st.session_state.pop('classification',None);st.error(str(e))
 r=st.session_state.get('classification')
 if r:
  m=r['metrics'];st.caption(f"Results: {r['algorithm']} predicting '{r['target']}'")
  st.dataframe(pd.DataFrame([{k:m[k] for k in ['Accuracy','Precision','Recall','F1','Kappa','AUC']}]),width='stretch')
  a,b=st.columns(2)
  a.plotly_chart(confusion_heatmap(m['Confusion Matrix'],r['classes']),width='stretch')
  with b:st.write('Classification Report');st.dataframe(pd.DataFrame(m['Report']).T,width='stretch')
  if r['tree_model'] is not None:st.subheader('Decision Tree Diagram');show_tree(r,'dm')
with t2:
 a=st.selectbox('Algorithm',['Apriori','FP-Growth']);s=st.slider('Minimum support',.01,1.,.1,.01);c=st.slider('Minimum confidence',.01,1.,.5,.01)
 if st.button('Mine Rules'):
  try:i,r=mine(df,a,s,c);st.session_state.rules=r;st.session_state.itemsets=i
  except Exception as e:st.error(str(e))
 if 'itemsets' in st.session_state:
  st.write('Frequent itemsets');st.dataframe(st.session_state.itemsets.astype(str),width='stretch')
  st.write('Rules');st.dataframe(st.session_state.rules.astype(str),width='stretch')
with t3:
 k=st.slider('K',2,10,3)
 if st.button('Run k-Means'):
  try:st.session_state.kmeans=kmrun(df,k)
  except Exception as e:st.error(str(e))
 if st.session_state.get('kmeans'):
  model,p,lab,sil=st.session_state.kmeans;x,y=st.columns(2);x.metric('SSE',round(model.inertia_,2));y.metric('Silhouette','N/A' if sil is None else round(sil,4));st.plotly_chart(cluster_scatter(p,lab),width='stretch')
 if st.button('Elbow Method'):
  try:st.session_state.elbow=elbow(df)
  except Exception as e:st.error(str(e))
 if st.session_state.get('elbow') is not None:
  e=st.session_state.elbow;st.plotly_chart(elbow_chart(e),width='stretch');st.dataframe(e,width='stretch')

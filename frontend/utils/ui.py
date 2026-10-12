import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))  # lets pages import backend.*
import streamlit as st
def load_css():
    p=Path(__file__).resolve().parents[1]/"assets"/"style.css"
    if p.exists(): st.markdown(p.read_text(encoding="utf-8"),unsafe_allow_html=True)
def hero(title,subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',unsafe_allow_html=True)
def section(title):
    st.markdown(f'<div class="section-title">{title}</div>',unsafe_allow_html=True)
def card(title,text,icon=""):
    st.markdown(f'<div class="card"><h3>{icon} {title}</h3><p>{text}</p></div>',unsafe_allow_html=True)
def workflow():
    items=["DATA","PREPROCESS","ETL","WAREHOUSE","OLAP","MINING","EVALUATION","REPORT"]
    html='<div class="workflow">'
    for i,x in enumerate(items):
        html+=f'<span class="step">{x}</span>'
        if i<len(items)-1: html+='<span class="arrow">→</span>'
    st.markdown(html+'</div>',unsafe_allow_html=True)

def show_tree(r,key="tree"):
    """Render the decision-tree diagram (interactive + static PNG) for a classification result."""
    from backend.visualization.charts import interactive_tree,static_tree_png
    m=r.get('tree_model')
    if m is None:
        st.info('Decision-tree diagrams are available for ID3, J48 and Random Forest.');return
    if r['algorithm'].lower()=='random forest':
        st.caption('Random Forest is an ensemble of 200 trees; the diagram shows the first tree as a representative example.')
    full=m.get_depth();c1,c2=st.columns([3,1])
    depth=c1.slider('Maximum depth to display',1,max(full,1),min(full,4),key=f'{key}_d') if full>1 else 1
    c2.metric('Tree depth / leaves',f'{full} / {m.get_n_leaves()}')
    st.plotly_chart(interactive_tree(m,r['feature_names'],r['classes'],depth),width='stretch',key=f'{key}_plotly')
    with st.expander('Static diagram (scikit-learn plot_tree) & text rules'):
        fig,png=static_tree_png(m,r['feature_names'],r['classes'],depth)
        st.pyplot(fig);st.download_button('Download tree as PNG',png,'decision_tree.png','image/png',key=f'{key}_png')
        import matplotlib.pyplot as plt;plt.close(fig)
        if r.get('tree'):st.code(r['tree'])

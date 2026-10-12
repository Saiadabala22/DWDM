# Integrated Data Warehousing & Data Mining Visualization System

Complete college DWDM project using Python, Streamlit and SQLite.

## Modules
Dataset Upload → Preprocessing → ETL → SQLite Data Warehouse → OLAP → Data Mining → Evaluation → Visualization → Final Report.

## Mining
Classification: ID3, J48, Naive Bayes, k-NN, Random Forest.
Association: Apriori, FP-Growth.
Clustering: k-Means with SSE/Elbow and silhouette score.

## Export
PDF, HTML, Excel, CSV, JSON.

## Setup & Run (Windows)
Open Command Prompt **inside this folder** (the one containing `manage.py`) and run:

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runstreamlit      (Streamlit app  -> http://localhost:8501)
    python manage.py runserver         (Django API/admin -> http://127.0.0.1:8000)

Or just double-click `setup_and_run.bat` (Mac/Linux: `./setup_and_run.sh`).
Optional: `python manage.py createsuperuser` for the Django admin. A sample dataset is in `sample_data/`.
(Equivalent without Django: `streamlit run frontend/app.py`.)

SQLite ships with Python, so there is no database server to install.

The warehouse is created automatically on first use at `data/dwdm_warehouse.db`
(schema in `backend/database/schema.sql`). Open it with "DB Browser for SQLite" if you want to inspect it.

## Visualization
The Visualization page reads straight from the SQLite warehouse (pick any table, 🔄 Refresh to reload), so it works even in a fresh session after a browser refresh. It can still chart the raw/ETL dataframes from the current session.
Decision trees (ID3, J48, one tree of a Random Forest) are drawn as an interactive Plotly diagram
(hover for samples/class mix, depth slider) plus a static scikit-learn diagram you can download as PNG.
The Visualization page (page 8, four tabs) has: missing-values, histogram, box, violin and density plots (Distributions); bar, pie, grouped/stacked bar and aggregate bars (Categories); correlation heatmap, scatter, line, scatter matrix, 3D scatter and parallel coordinates (Relationships); plus mining results. It also has distributions, category charts, correlation heatmap, scatter plots,
confusion matrix, feature importance, k-means clusters, elbow curve and association-rule plots.

J48 is implemented with an entropy-based pruned-style decision tree configuration in Python. The architecture can later be connected to native Weka J48 if exact Weka output is required.

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def _matrix(df):
    X = pd.get_dummies(df, dtype=float)
    if X.shape[1] == 0 or len(X) < 3:
        raise ValueError('Need at least 3 rows and 1 column for clustering.')
    X = SimpleImputer(strategy='median').fit_transform(X)
    return StandardScaler().fit_transform(X)


def _sil(X, labels):
    if len(set(labels)) < 2 or len(X) <= len(set(labels)):
        return None
    return float(silhouette_score(X, labels, sample_size=min(len(X), 5000), random_state=42))


def run(df, k):
    X = _matrix(df)
    k = min(k, len(X) - 1)
    model = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    labels = model.labels_
    p = PCA(n_components=min(2, X.shape[1]), random_state=42).fit_transform(X)
    if p.shape[1] == 1:
        p = np.column_stack([p[:, 0], np.zeros(len(p))])
    return model, p, labels, _sil(X, labels)


def elbow(df, kmax=10):
    X = _matrix(df)
    rows = []
    for k in range(2, min(kmax, len(X) - 1) + 1):
        m = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
        rows.append({'K': k, 'SSE': m.inertia_, 'Silhouette': _sil(X, m.labels_)})
    return pd.DataFrame(rows)

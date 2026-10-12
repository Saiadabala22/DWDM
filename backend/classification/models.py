import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, cohen_kappa_score,
                             confusion_matrix, classification_report, roc_auc_score)

TREE_ALGS = ("id3", "j48")


def _prep(num, cat, scale):
    steps = [('impute', SimpleImputer(strategy='median'))] + ([('scale', StandardScaler())] if scale else [])
    return ColumnTransformer([
        ('num', Pipeline(steps), num),
        ('cat', Pipeline([('impute', SimpleImputer(strategy='most_frequent')),
                          ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), cat)])


def _feature_names(prep, num, cat):
    """Readable names: numeric -> 'col', one-hot -> 'col = value'."""
    try:
        cats = prep.named_transformers_['cat'].named_steps['onehot'].categories_
        names = list(num) + [f'{c} = {v}' for c, vals in zip(cat, cats) for v in vals]
        if len(names) == len(prep.get_feature_names_out()):
            return names
    except Exception:
        pass
    return [n.split('__', 1)[-1] for n in prep.get_feature_names_out()]


def run(df, target, algorithm):
    X = df.drop(columns=[target])
    y = df[target].astype(str)
    le = LabelEncoder()
    yy = le.fit_transform(y)
    cat = X.select_dtypes(exclude='number').columns.tolist()
    num = X.select_dtypes('number').columns.tolist()
    if not len(X.columns):
        raise ValueError('Need at least one feature column besides the target.')
    try:
        Xtr, Xte, ytr, yte = train_test_split(X, yy, test_size=.2, random_state=42, stratify=yy)
    except ValueError:  # a class too small to stratify
        Xtr, Xte, ytr, yte = train_test_split(X, yy, test_size=.2, random_state=42)
    a = algorithm.lower()
    tree_model = a in TREE_ALGS
    # Trees are not scaled so split thresholds in the diagram are in original units.
    prep = _prep(num, cat, scale=not tree_model)
    if a == 'id3':
        est = DecisionTreeClassifier(criterion='entropy', random_state=42)
    elif a == 'j48':
        est = DecisionTreeClassifier(criterion='entropy', min_samples_leaf=2, ccp_alpha=0.001, random_state=42)
    elif a == 'naïve bayes':
        est = GaussianNB()
    elif a == 'k-nn':
        est = KNeighborsClassifier(min(5, len(ytr)))
    else:
        est = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    model = Pipeline([('prep', prep), ('model', est)])
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    proba = model.predict_proba(Xte)
    feature_names = _feature_names(prep, num, cat)

    tree = None
    tree_model_obj = None
    importances = None
    if tree_model:
        tree_model_obj = est
        tree = export_text(est, feature_names=feature_names)
    elif a == 'random forest':
        tree_model_obj = est.estimators_[0]  # one representative tree of the forest
    if hasattr(est, 'feature_importances_'):
        importances = (pd.DataFrame({'Feature': feature_names, 'Importance': est.feature_importances_})
                       .sort_values('Importance', ascending=False).reset_index(drop=True))

    m = {'Accuracy': accuracy_score(yte, pred),
         'Precision': precision_score(yte, pred, average='weighted', zero_division=0),
         'Recall': recall_score(yte, pred, average='weighted', zero_division=0),
         'F1': f1_score(yte, pred, average='weighted', zero_division=0),
         'Kappa': cohen_kappa_score(yte, pred),
         'Confusion Matrix': confusion_matrix(yte, pred, labels=range(len(le.classes_))),
         'Report': classification_report(yte, pred, labels=range(len(le.classes_)), target_names=[str(c) for c in le.classes_],
                                         output_dict=True, zero_division=0)}
    try:
        m['AUC'] = (roc_auc_score(yte, proba, multi_class='ovr', labels=range(len(le.classes_)))
                    if len(le.classes_) > 2 else roc_auc_score(yte, proba[:, 1]))
    except Exception:
        m['AUC'] = None
    return {'metrics': m, 'classes': le.classes_, 'tree': tree, 'tree_model': tree_model_obj,
            'feature_names': feature_names, 'importances': importances, 'algorithm': algorithm,
            'target': target, 'proba': proba, 'pred': pred, 'y': yte}

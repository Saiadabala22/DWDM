import pandas as pd
from sklearn.preprocessing import StandardScaler

_NA_TOKENS = {'', 'na', 'n/a', 'nan', 'null', 'none', '?', '-', '--', 'missing', 'unknown'}


def infer_types(df, threshold=0.9):
    """Convert text columns that really hold numbers (e.g. '1,200', '45%', '$300', ' 5.1 ', '?') to numeric.

    A column is converted when at least `threshold` of its non-missing values parse as numbers.
    Columns that are genuinely categorical are left untouched.
    """
    x = df.copy()
    for c in x.columns:
        if pd.api.types.is_numeric_dtype(x[c]) or pd.api.types.is_bool_dtype(x[c]):
            continue
        s = x[c].astype('string').str.strip()
        s = s.mask(s.str.lower().isin(_NA_TOKENS))
        present = s.notna()
        if not present.any():
            continue
        t = (s.str.replace(r'[,\s]', '', regex=True)
              .str.replace(r'^[\$€£₹¥]', '', regex=True)
              .str.replace(r'%$', '', regex=True)
              .str.replace(r'^\((.*)\)$', r'-\1', regex=True))
        num = pd.to_numeric(t, errors='coerce')
        if num[present].notna().mean() >= threshold:
            x[c] = num.astype('float64')
            if not x[c].isna().any() and x[c].apply(float.is_integer).all():
                x[c] = x[c].astype('int64')
    return x

def clean(df,encode=True,scale=False,duplicates=True):
    x=infer_types(df); before=len(x)
    if duplicates:x=x.drop_duplicates()
    for c in x.columns:
        if x[c].isna().any():
            if pd.api.types.is_numeric_dtype(x[c]):x[c]=x[c].fillna(x[c].median())
            else:
                m=x[c].mode();x[c]=x[c].fillna(m.iloc[0] if len(m) else 'Unknown')
    if encode:
        cats=x.select_dtypes(exclude='number').columns
        if len(cats):x=pd.get_dummies(x,columns=cats,dtype=float)
    if scale:
        nums=x.select_dtypes('number').columns
        if len(nums):x[nums]=StandardScaler().fit_transform(x[nums])
    return x,{'rows_before':before,'rows_after':len(x),'duplicates_removed':before-len(x)}

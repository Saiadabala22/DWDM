import io,zipfile,pandas as pd
from backend.preprocessing.preprocessing import infer_types
def load_dataset(f):
    return infer_types(_load(f))
def _load(f):
    n=f.name.lower(); b=f.getvalue()
    if n.endswith('.csv'): return pd.read_csv(io.BytesIO(b))
    if n.endswith(('.xls','.xlsx')): return pd.read_excel(io.BytesIO(b))
    if n.endswith('.arff'):
        try:
            import arff
        except ImportError:
            raise ImportError('ARFF support needs the liac-arff package: pip install liac-arff')
        o=arff.load(io.StringIO(b.decode('utf8',errors='ignore'))); return pd.DataFrame(o['data'],columns=[a[0] for a in o['attributes']])
    if n.endswith('.zip'):
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            fs=[x for x in z.namelist() if x.lower().endswith(('.csv','.xls','.xlsx','.arff'))]
            if not fs: raise ValueError('ZIP contains no supported dataset.')
            class F:
                name=fs[0]
                def getvalue(self): return z.read(fs[0])
            return _load(F())
    raise ValueError('Unsupported file type.')
def summary(df): return {'Rows':len(df),'Columns':len(df.columns),'Missing':int(df.isna().sum().sum()),'Duplicates':int(df.duplicated().sum())}

import pandas as pd
def slice_df(df,col,val):return df[df[col].astype(str)==str(val)]
def dice(df,filters):
    x=df
    for c,v in filters.items():
        if v:x=x[x[c].astype(str).isin([str(a) for a in v])]
    return x
def aggregate(df,dims,measure,agg='sum'):return df.groupby(dims,dropna=False)[measure].agg(agg).reset_index() if dims else pd.DataFrame({measure:[getattr(df[measure],agg)()]})
def rollup(df,hierarchy,measure,agg='sum'):
    return pd.concat([aggregate(df,hierarchy[:i],measure,agg).assign(level=i) for i in range(1,len(hierarchy)+1)],ignore_index=True)
def pivot(df,index,columns,values,agg='sum'):return pd.pivot_table(df,index=index,columns=columns,values=values,aggfunc=agg,fill_value=0).reset_index()

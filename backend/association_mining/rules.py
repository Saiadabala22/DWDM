import pandas as pd
from mlxtend.frequent_patterns import apriori,fpgrowth,association_rules
def mine(df,algorithm,support,confidence):
    tx=pd.get_dummies(df.astype(str))
    items=(apriori if algorithm=='Apriori' else fpgrowth)(tx,min_support=support,use_colnames=True)
    rules=association_rules(items,metric='confidence',min_threshold=confidence) if len(items) else pd.DataFrame()
    return items,rules

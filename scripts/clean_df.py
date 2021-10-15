# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 09:34:49 2021

@author: felip
"""

import pandas as pd

kraken = pd.read_excel('kraken_close.xlsx')
coinbase = pd.read_excel('coinbase_close.xlsx')

coins = []

for i in kraken:
    if i in coinbase.columns:
        coins.append(i)
        
# %%
coinbase = coinbase[coins].set_index('date')
kraken = kraken[coins].set_index('date')

coinbase_cols = list(map(lambda x: ('coinbase', x), coinbase.columns))
kraken_cols = list(map(lambda x: ('kraken', x), kraken.columns))

coinbase_cols = pd.MultiIndex.from_tuples(coinbase_cols, names=["exchange", "crypto"])
kraken_cols = pd.MultiIndex.from_tuples(kraken_cols, names=["exchange", "crypto"])

coinbase.columns = coinbase_cols
kraken.columns = kraken_cols

df = pd.concat([kraken, coinbase],axis=1).dropna()


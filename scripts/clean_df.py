import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

os.chdir(r'C:\Users\felip\OneDrive\Documentos\UBRI\ubri-research\scripts')

kraken = pd.read_excel('kraken_close.xlsx')
coinbase = pd.read_excel('coinbase_close.xlsx')

coins = []

for i in kraken:
    if i in coinbase.columns:
        coins.append(i)
        
# %%

'''

Cria dataframe com duas bolsas e aplica log nos preços

'''
coinbase = coinbase[coins].set_index('date')
kraken = kraken[coins].set_index('date')

coinbase_cols = list(map(lambda x: ('coinbase', x), coinbase.columns))
kraken_cols = list(map(lambda x: ('kraken', x), kraken.columns))

coinbase_cols = pd.MultiIndex.from_tuples(coinbase_cols, names=["exchange", "crypto"])
kraken_cols = pd.MultiIndex.from_tuples(kraken_cols, names=["exchange", "crypto"])

coinbase.columns = coinbase_cols
kraken.columns = kraken_cols

df = pd.concat([kraken, coinbase],axis=1).dropna()

df = np.log(df)

# %%

'''

Visualizando dados

'''

fig, axs = plt.subplots(2,1,figsize=(10,10))

df.kraken.plot(ax=axs[0], legend=False)

df.coinbase.plot(ax=axs[1])

plt.legend(bbox_to_anchor=(1.01, 1.5), loc='upper left', borderaxespad=0)


# %%

print(df.kraken.describe().round(3).T.drop('count',axis=1).to_latex())

print(df.coinbase.describe().round(3).T.drop('count',axis=1).to_latex())

# %%



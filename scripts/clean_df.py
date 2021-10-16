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
axs[0].set_title('Kraken', loc='left', fontsize=16)
df.kraken.plot(ax=axs[0], legend=False)

df.coinbase.plot(ax=axs[1])
axs[1].set_title('Coinbase', loc='left', fontsize=16)
plt.legend(bbox_to_anchor=(1.01, 1.5), loc='upper left', borderaxespad=0)


# %%
'''

Descrição dos dados

'''
print(df.kraken.describe().round(3).T.drop('count',axis=1).to_latex())

print(df.coinbase.describe().round(3).T.drop('count',axis=1).to_latex())

# %%

adf_kraken = pd.DataFrame()

adf_coinbase = pd.DataFrame()

for coin in coins[1:]:

    adf = adfuller(df.kraken[coin])

    adf_kraken[coin] = pd.Series(list(adf[:2]), index = ['adf', 'pvalue'])
    
    adf = adfuller(df.coinbase[coin])
    
    adf_coinbase[coin] = pd.Series(list(adf[:2]), index = ['adf', 'pvalue'])

    
# %%

print(adf_kraken.T.round(3).to_latex())

print(adf_coinbase.T.round(3).to_latex())


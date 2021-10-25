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

df = pd.concat([kraken, coinbase],axis=1)#.dropna()

df = np.log(df)

for i in df.columns.get_level_values('crypto'):
    sliced_coin = df.xs(i,level=1, axis=1).dropna()
    df.loc[:,('kraken',i)] = sliced_coin['kraken']
    df.loc[:,('coinbase',i)] = sliced_coin['coinbase']

df = df.loc[df.first_valid_index():]
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
kraken_desc = df.kraken.describe().round(3).T
kraken_desc['count'] = kraken_desc['count'].apply(int)


coinbase_desc = df.coinbase.describe().round(3).T
coinbase_desc['count'] = coinbase_desc['count'].apply(int)


print(kraken_desc.to_latex())
print(coinbase_desc.to_latex())

# %%

def add_star(pvalue : float) -> str:
    
    ast = ''
    
    if pvalue < 0.1:
        ast = '*'
    
    if pvalue < 0.05:
        ast = '**'
        
    if pvalue < 0.05:
        ast = '**'
        
    if pvalue < 0.01:
        ast = '***'
            
    return str(pvalue)[:6] + ast

# %%

adf_kraken = pd.DataFrame()

adf_coinbase = pd.DataFrame()

for coin in coins[1:]:
    
    

    adf = list(adfuller(df.kraken[coin].dropna()))
    #adf[1] = add_star(adf[1])    
    adf = adf[:3]#, *adf[4].values(), adf[5]]    
    adf_kraken[coin] = pd.Series(adf, index = ['adf', 'pvalue', 'lag'])
    
    adf = list(adfuller(df.coinbase[coin].dropna()))
    #adf[1] = add_star(adf[1])
    adf = adf[:3]#, *adf[4].values(), adf[5]]
    adf_coinbase[coin] = pd.Series(adf, index = ['adf', 'pvalue', 'lag'])
    
    
# %%
adf_table_kraken = adf_kraken.T.round(3)
adf_table_kraken.pvalue = adf_table_kraken.pvalue.apply(add_star)
print(adf_table_kraken.to_latex())


adf_table_coinbase = adf_coinbase.T.round(3)
adf_table_coinbase.pvalue = adf_table_coinbase.pvalue.apply(add_star)
print(adf_table_coinbase.to_latex())


# %%
dff = df.diff().dropna()


'''

Visualizando dados 1 diferenças

'''

fig, axs = plt.subplots(2,1,figsize=(10,10))
axs[0].set_title('Kraken', loc='left', fontsize=16)
dff.kraken.plot(ax=axs[0], legend=False)

dff.coinbase.plot(ax=axs[1])
axs[1].set_title('Coinbase', loc='left', fontsize=16)
plt.legend(bbox_to_anchor=(1.01, 1.5), loc='upper left', borderaxespad=0)

# %%

adff_kraken = pd.DataFrame()

adff_coinbase = pd.DataFrame()

for coin in coins[1:]:
    
    

    adf = list(adfuller(dff.kraken[coin].dropna()))   
    adf = adf[:3]#, *adf[4].values(), adf[5]]    
    adff_kraken[coin] = pd.Series(adf, index = ['adf', 'pvalue', 'lag'])
                                                         
    
    adf = list(adfuller(dff.coinbase[coin].dropna()))
    adf = adf[:3]#, *adf[4].values(), adf[5]] 
    adff_coinbase[coin] = pd.Series(adf, index = ['adf', 'pvalue', 'lag'])
    
# %%
adff_table_kraken = adff_kraken.T.round(3)
adff_table_kraken.pvalue = adff_table_kraken.pvalue.apply(add_star)
print(adff_table_kraken.to_latex())


adff_table_coinbase = adff_coinbase.T.round(3)
adff_table_coinbase.pvalue = adff_table_coinbase.pvalue.apply(add_star)
print(adff_table_coinbase.to_latex())


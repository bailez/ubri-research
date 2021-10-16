import os
os.chdir(r'C:\Users\felip\OneDrive\Documentos\UBRI\ubri-research\scripts')
from coinbase import get_coinbase
from kraken import get_kraken
import pandas as pd
from coins import COINS

COINS

begin = '2010-01-01'
end = '2021-12-31'
min_obs = 200
index = 'close'

# %% COINBASE

writer = pd.ExcelWriter('coinbase.xlsx', engine='xlsxwriter')

for coin in COINS:   

    crypto = (COINS[coin])
    

    df = get_coinbase(begin, end, crypto, debug = True)
    
    if len(df) == 0:
        continue
        
    if len(df[index].dropna()) < min_obs:
        print(coin, 'tem poucas observações')
        continue


    df.to_excel(writer, sheet_name = coin + f' ({crypto})')

writer.save()

# %%



writer = pd.ExcelWriter(f'coinbase_{index}.xlsx', engine='xlsxwriter')

df_close = pd.DataFrame()

for coin in COINS:   

    crypto = (COINS[coin])

    temp = get_coinbase(begin, end, crypto, debug = True)
    
    if len(temp) == 0:
        continue
    
    if len(temp[index].dropna()) < min_obs:
        print(coin, 'tem poucas observações')
        continue
    
    df_close[crypto] = temp[index]
    


df_close.to_excel(writer, sheet_name = index)

writer.save()

# %% Kraken

writer = pd.ExcelWriter('kraken.xlsx', engine='xlsxwriter')

for coin in COINS:   

    crypto = (COINS[coin])

    df = get_kraken(crypto, debug = True)
    
    if len(df) == 0:
        continue    
    
    if len(df[index].dropna()) < min_obs:
        print(coin, 'tem poucas observações')
        continue

    df.to_excel(writer, sheet_name = coin + f' ({crypto})')

writer.save()

# %% 

index = 'close'

writer = pd.ExcelWriter(f'kraken_{index}.xlsx', engine='xlsxwriter')

df_close = pd.DataFrame()

for coin in COINS:   

    crypto = (COINS[coin])

    temp = get_kraken(crypto, debug = True)
    if len(temp) == 0:
        continue
    
    if len(temp[index].dropna()) < min_obs:
        print(coin, 'tem poucas observações')
        continue
    df_close[crypto] = temp[index]

    
# %%

df_close.to_excel(writer, sheet_name = index)

writer.save()
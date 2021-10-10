from coinbase import get_coin_series
import pandas as pd
from coins import COINS

COINS

begin = '2010-01-01'
end = '2021-12-31'


# COINBASE

writer = pd.ExcelWriter('coinbase.xlsx', engine='xlsxwriter')

for coin in COINS:   

    crypto = (COINS[coin])

    df = get_coin_series(begin, end, crypto)

    df.to_excel(writer, sheet_name = coin)

writer.save()
import pandas as pd
import requests



def get_coinbase(crypto : str, 
                 start_date : str, end_date : str,
                 fiat : str = 'USD',
                 granularity : str = '86400') -> pd.DataFrame:

    symbol = crypto + '-' + fiat
    
    url = f'https://api.exchange.coinbase.com/products/{symbol}/candles?'\
    f'granularity={granularity}&start={start_date}&end={end_date}' 
    
    #url = 'https://api.binance.com/api/v1/klines?symbol=ETHBTC&interval=4h'
    
    response = requests.get(url)
    
    df = pd.read_json(response.text)
    
    df.columns=['unix', 'low', 'high', 'open', 'close', 'volume']

    df['date'] = pd.to_datetime(df['unix'], unit='s')
    
    return df



df = get_coinbase(crypto = 'BTC', 
                  start_date = '01-01-2021', 
                  end_date = '10-01-2021')

# %%

url = 'https://api.binance.com/api/v1/klines?symbol=BTCUSDT&interval=1d'

response = requests.get(url)

df = pd.read_json(response.text)

df.columns = ['open time', 'open', 'high', 'low', 'close', 'volume', 'close time', 
 'volume', 'trades', 'base volume', 'quote volume', 'ignore']


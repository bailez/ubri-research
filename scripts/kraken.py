import pandas as pd
import requests
import json


def _kraken_wrapper(crypto : str, 
                 since : str = '1437350400',
                 fiat : str = 'USD',
                 timeframe : str = '1440',
                 debug : bool = False) -> pd.DataFrame:

    
    
    symbol = crypto + fiat  
    
    
    url = f'https://api.kraken.com/0/public/OHLC?pair={symbol}&interval={timeframe}&since=1437350400'
    
    response = requests.get(url)
    
    j = json.loads(response.text)
    
    try:
        result = j['result']
    except KeyError as e:
        
        if debug:
            
            print(e)
            
        return None
    
    keys = list(result.keys())
    
    raw_data = result[keys[0]] if keys[0] != 'last' else result[keys[1]]
    
        
    df = pd.DataFrame(raw_data)
    
    df.columns = ['unix', 'open', 'high', 'low', 'close', 
                  'vwap', 'volume', 'tradecount']
    
    df['date'] = pd.to_datetime(df['unix'], unit='s')
    
    return df



def get_kraken(crypto : str, 
                    debug : bool = False) -> pd.DataFrame:
    
    
    df = _kraken_wrapper(crypto = crypto)
    
    if type(df) == type(None):
        return pd.DataFrame()
            
    df = df.set_index('date')
           
    #df = df.drop('unix',axis=1)
    
    df = df[~df.index.duplicated(keep='first')]
    
    df = df.sort_index()
    
    return df
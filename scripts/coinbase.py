import pandas as pd
import requests



def _coinbase_wrapper(crypto : str, 
                 start_date : str, end_date : str,
                 fiat : str = 'USD',
                 granularity : str = '86400',
                 debug : bool = False) -> pd.DataFrame:

    symbol = crypto + '-' + fiat
    
    url = f'https://api.exchange.coinbase.com/products/{symbol}/candles?'\
    f'granularity={granularity}&start={start_date}&end={end_date}' 
    
    response = requests.get(url)
    try:
        df = pd.read_json(response.text)
    except ValueError as e:
        if debug:
            print(crypto, response.text)
        
        return None
    
    df.columns=['unix', 'low', 'high', 'open', 'close', 'volume']

    df['date'] = pd.to_datetime(df['unix'], unit='s')
    
    return df

def get_coinbase(begin : str, end : str, 
                    crypto : str, debug : bool = False) -> pd.DataFrame:
    
    dates = pd.date_range(begin, end)
    
    df = pd.DataFrame()
    
    for i in range(len(dates)//300):
    
        start_date = dates[i*300]
    
        end_date = dates[(i+1)*300]
    
    
        try:   
            df_slice = _coinbase_wrapper(crypto = crypto, 
                      start_date = start_date, 
                      end_date = end_date,
                      debug = debug)
        except ValueError as e:
            if debug:
                print(crypto, start_date, end_date)
                print(e)               
            
            continue
                
        
        df = pd.concat([df, df_slice], axis=0)
        
    df_slice = _coinbase_wrapper(crypto = 'BTC', 
                  start_date = end_date, 
                  end_date = dates[-1])
    
    df = pd.concat([df, df_slice], axis=0)
    
    df = df.set_index('date')
           
    #df = df.drop('unix',axis=1)
    
    df = df[~df.index.duplicated(keep='first')]
    
    df = df.sort_index()
    
    return df


import os
import pandas as pd
from functions import *

os.chdir(r'C:\Users\felip\OneDrive\Documentos\UBRI\ubri-research\scripts')


exchange_1_name = 'kraken'

exchange_2_name = 'coinbase'

exchange_1 = pd.read_excel('kraken_close.xlsx')
exchange_2 = pd.read_excel('coinbase_close.xlsx')

df = generate_dataframe(exchange_1, exchange_2, 
                        exchange_1_name, exchange_2_name)

plot_series(df, exchange_1_name, exchange_2_name)

exchange_1_desc,exchange_2_desc = print_description(df, 
                                                    exchange_1_name,
                                                    exchange_2_name)



ct_adf_table_1, ct_adf_table_2 = adf_test(df, 
                                    exchange_1_name, 
                                    exchange_2_name , 
                                    'ct' )

n_adf_table_1, n_adf_table_2 = adf_test(df, 
                                    exchange_1_name, 
                                    exchange_2_name , 
                                    'n' )



df_fd = df.diff()

plot_series(dff, exchange_1_name, exchange_2_name)


ct_adff_table_1, ct_adff_table_2 = adf_test(dff, 
                                    exchange_1_name, 
                                    exchange_2_name , 
                                    'ct' )

n_adff_table_1, n_adff_table_2 = adf_test(dff, 
                                    exchange_1_name, 
                                    exchange_2_name , 
                                    'n' )


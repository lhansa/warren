import pandas as pd
from yahoofinancials import YahooFinancials
import matplotlib.pyplot as plt

#%% Funciones guays
def prep_df(simbolo):
    yf= YahooFinancials(simbolo)
    data= yf.get_historical_price_data(
        start_date='2019-01-01',
        end_date='2020-08-31', 
        time_interval='daily'
    ) 
 
    df= pd.DataFrame(data[simbolo]['prices'])
    df['symb'] = simbolo
    df= df.drop('date', axis=1).set_index(['symb', 'formatted_date'])

    return df

#%% Simbolos

# Amadeus AMS.MC
# Yonghui 601933.SS

simbolos = ['AMS.MC', '601933.SS']

l_dfs = list(map(prep_df, simbolos))

#%% Agregación
df_todo = pd.concat(l_dfs)
df_todo_wide = df_todo.reset_index(drop=False).pivot(index='formatted_date', columns='symb', values='close')

#%% Visualización
df_todo_wide.plot(subplots=True, ylim=(0,None))
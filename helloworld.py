import pandas as pd
from yahoofinancials import YahooFinancials
import matplotlib.pyplot as plt
from datetime import date

#%% Funciones guays
def prep_df(simbolo, valores, start='2020-01-01'):
    yf = YahooFinancials(simbolo)
    data= yf.get_historical_price_data(
        start_date=start,
        end_date=date.today().strftime('%Y-%m-%d'), 
        time_interval='daily'
    ) 
 
    df= pd.DataFrame(data[simbolo]['prices'])
    df['valor'] = valores
    df= df.drop('date', axis=1).set_index(['valor', 'formatted_date'])

    return df

#%% Simbolos
valores = {'Amadeus':'AMS.MC', 
           'Yonghui':'601933.SS', 
           'Cisco':'CSCO', 
           'Lenovo':'0992.HK'}

#%% Preparación de parámetros
simbolos = list(valores.values())
l_valores = list(valores.keys())
fecha_ini = ['2020-06-01'] * len(simbolos)

#%% Descarga de datos
l_dfs = list(map(prep_df, simbolos, l_valores, fecha_ini))

#%% Agregación
df_todo = pd.concat(l_dfs)
df_todo_wide = df_todo.reset_index(drop=False).pivot(index='formatted_date', columns='valor', values='close')

#%% Visualización
df_todo_wide.plot(subplots=True, ylim=(None,None))
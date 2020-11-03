import pandas as pd
from yahoofinancials import YahooFinancials
import matplotlib.pyplot as plt
from datetime import date

#%% Funciones guays
def prep_df(simbolo, d_valor, start='2020-01-01'):
    yf = YahooFinancials(simbolo)
    data= yf.get_historical_price_data(
        start_date=start,
        end_date=date.today().strftime('%Y-%m-%d'), 
        time_interval='daily'
    ) 
 
    df= pd.DataFrame(data[simbolo]['prices'])
    df['valor'] = d_valor['name']
    df= df.drop('date', axis=1).set_index(['valor', 'formatted_date'])

    return df

#%% Simbolos
cartera_warren = {
    'AAPL' : {
        'name' : 'Apple',
        'perc': 0.4418,
        'shares': 980622264
    },
    'BAC' : {
        'name' : 'Bank of America', 
        'perc': 0.1085, 
        'shares' : 925008600
    }, 
    'KO' : {
        'name' : 'Coca Cola',
        'perc': 0.0883, 
        'shares' : 400000000 
    }, 
    'AXP' : {
        'name': 'American Express',
        'perc' : 0.0713, 
        'shares' : 151610700
    }, 
    'KHC' : {
        'name' : 'Kraft Heinz', 
        'perc' : 0.0514, 
        'shares' : 325634818
    }, 
    'MCO' : {
        'name' : 'Moodys',
        'perc': 0.0335, 
        'shares': 24669778
    }
}

#%% Preparación de parámetros
simbolos = list(cartera_warren.keys())
l_valores = list(cartera_warren.values())
fecha_ini = ['2020-01-01'] * len(cartera_warren)

#%% Descarga de datos
l_dfs = list(map(prep_df, simbolos, l_valores, fecha_ini))

#%% Agregación
df_todo = pd.concat(l_dfs)
df_todo_wide = df_todo.reset_index(drop=False).pivot(index='formatted_date', columns='valor', values='close')

#%% Visualización
df_todo_wide.plot(subplots=True, ylim=(None,None))


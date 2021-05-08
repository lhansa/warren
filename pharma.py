import pandas as pd
from yahoofinancials import YahooFinancials
import matplotlib.pyplot as plt
from datetime import date

#%% Init things
fecha_ini = '2019-10-01'
fecha_fin = date.today().strftime('%Y-%m-%d')

precio_referencia = 'close'

ticker_list = ['MRNA', 'PFE', 'JNJ', 'AZN']

#%% Define functions
def prep_evol_df(ticker):
    yh = YahooFinancials(ticker)
    data = yh.get_historical_price_data(
        start_date=fecha_ini, 
        end_date=fecha_fin, 
        time_interval='daily'
    )

    df = pd.DataFrame(data[ticker]['prices'])
    df['ticker'] = ticker
    df['formatted_date'] = df['formatted_date'].apply(pd.Timestamp)
    df = df.drop(
        ['date', 'adjclose'], 
        axis=1
    ).rename(
        columns={'formatted_date':'date'}
    ).set_index(['ticker','date'])
    
    return df

#%% Create master data frame
df_master = pd.concat(map(prep_evol_df, ticker_list))

# Compute market capitalization
df_master['market_cap'] = df_master[precio_referencia] * df_master['volume']

#%% Price evolution
df_close_wide = df_master.reset_index(drop=False).pivot(
    index='date', 
    columns='ticker',
    values=precio_referencia
)

df_close_wide.plot(subplots=True, kind='line')
plt.axvline(x=pd.Timestamp('2021-03-01'),
            ymax=max(df_master[precio_referencia]),
            color='darkblue')
plt.show()

# TODO
# - Estudiar dispersiones
# - Estudiar variación desde declaración pandemia

#%% Market Cap evolution
df_cap_wide = df_master.reset_index(drop=False).pivot(
    index='date', 
    columns='ticker',
    values='market_cap'
)

df_cap_wide.plot(subplots=True, kind='line')
plt.axvline(x=pd.Timestamp('2021-03-01'),
            ymax=max(df_master[precio_referencia]),
            color='darkblue')
plt.show()

import requests
import json
import pandas as pd
import pytz
from dmi_open_data import DMIOpenDataClient, Parameter, ClimateDataParameter
import os
import datetime
print(os.getcwd())
print(os.getenv('PYTHONPATH'))
import data_reader
import matplotlib.pyplot as plt


fd=datetime.datetime(2024,8,1,0,0,0)
td=datetime.datetime(2024,9,1,0,0,0)
data_reader=data_reader.DataReader()
df_energinet, df_energinet_properties = data_reader.production_data(from_date=fd, 
                        to_date=td, 
                        price_area='DK2')

df_stations = data_reader.dmi_stations(only_dmi=True, parameter='wind_speed')


df_observations=pd.DataFrame()
for idx, dmi_station in df_stations.iterrows():
    print (dmi_station['properties.name'])
    df_ = data_reader.dmi_observations(from_date=fd,to_date=td, 
        station_id=dmi_station['properties.stationId'],
        station_name=dmi_station['properties.name'],
        parameter=Parameter.WindSpeed)
    if df_ is not None: 
        df_observations=pd.concat([df_observations,df_[['fromDatetime','value','station_name','station_id']]])
    pass

df_stat=df_energinet.query(''' property=='OnshoreWindGe50kW_MWh' ''').rename(columns={'value':'production'}).\
        merge(df_observations.rename(columns={'value':'wind_speed'}), on='fromDatetime')
df_corr=df_stat.groupby(['station_name'])[['production','wind_speed']].corr().reset_index().query(''' level_1 == 'production' ''').sort_values('wind_speed').reset_index()

station = df_corr.loc[0]['station_name']
df_graph= df_stat.query(''' station_name == @station ''')
plt.scatter(df_graph['wind_speed'],df_graph['production'])
plt.savefig('test/mincorr.png')
plt.clf()

station = df_corr.loc[df_corr.shape[0]-1]['station_name']
df_graph= df_stat.query(''' station_name == @station ''')
plt.scatter(df_graph['wind_speed'],df_graph['production'])
plt.savefig('test/maxcorr.png')
plt.clf()

# .plot.scatter(x='wind_speed',y='production')
pass
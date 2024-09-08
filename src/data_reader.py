import requests
import json
import pandas as pd
import pytz
from dmi_open_data import DMIOpenDataClient, Parameter, ClimateDataParameter
import os
import datetime


class DataReader:
    def __init__(self):
        self.dmi_client =  DMIOpenDataClient(api_key=os.getenv('DMI_API_KEY'))
        self.energinet_url = 'https://api.energidataservice.dk/dataset/'
     
    def dmi_stations(self, only_dmi=True, parameter='wind_speed'):
        stations = self.dmi_client.get_stations()
        df_stations=pd.json_normalize(stations)
        for idx, row in df_stations.iterrows():
            df_stations.loc[idx,'include']=parameter in row['properties.parameterId']
        if only_dmi:
            dmi_stations_=df_stations.query(''' include == True & `properties.owner`.str.lower() == 'dmi'  ''').copy().drop_duplicates(subset=['properties.name','properties.stationId'])
        else:
            dmi_stations_=df_stations.query(''' include == True  ''').copy().drop_duplicates(subset=['properties.name','properties.stationId'])
        return dmi_stations_

    def dmi_observations(self, from_date=None, to_date=None, station_id=None, station_name=None,parameter=None, observation_name=None ):
        
        observations = self.dmi_client.get_observations(
        station_id=station_id,
        parameter=parameter,
        from_time=from_date,
        to_time=to_date)
        df=None
        if len(observations)>0:
            df= pd.json_normalize(observations)
            df['fromDatetime']=pd.to_datetime(df['properties.observed'])
            df['value']=df['properties.value'].astype(float)
            df['station_name']=station_name
            df['station_id']=station_id
            df['parameter']=df['properties.parameterId']
        return df


     
    def production_data(self,from_date=datetime.datetime(2024,8,1,0,0,0),to_date=datetime.datetime(2024,9,1,0,0,0),price_area='DK2'):
        url_string = '''{url}ProductionConsumptionSettlement?offset=0&start={fd}&end={td}&filter=%7B%22PriceArea%22:[%22{pricearea}%22,%22%22]%7D&sort=HourUTC%20DESC'''
        url_string = url_string.format(url=self.energinet_url,fd=from_date.strftime('%Y-%m-%dT%H:%M'),
                       td=to_date.strftime('%Y-%m-%dT%H:%M'),pricearea=price_area)
        r = requests.get(url_string, timeout=60)
        dict_ =json.loads(r.text)
        df_dict = dict_['records']
        df=pd.DataFrame.from_dict(df_dict)
        df['fromDatetime'] = pd.to_datetime(df['HourUTC']).dt.tz_localize(pytz.UTC)
        df=df.drop(columns=['HourUTC','HourDK'])
        properties=df.drop(columns='fromDatetime').columns
        df=df.melt(id_vars=['fromDatetime','PriceArea'],var_name='property',value_name='value').sort_values(['property','fromDatetime'])
        return df,properties
        # df=df.rename(columns={'OnshoreWindGe50kW_MWh':'production'})[['fromDatetime','production']]
        # https://api.energidataservice.dk/dataset/ProductionConsumptionSettlement?offset=0&sort=HourUTC%20DESC
        # r = requests.get(self.energinet_urlProductionConsumptionSettlement?offset=0&start=2024-08-01T00:00&end=2024-09-01T00:00&filter=%7B%22PriceArea%22:[%22DK2%22,%22%22]%7D&sort=HourUTC%20DESC')
        
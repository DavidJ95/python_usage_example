   
import sys
import getopt
import pandas as pd
import datetime
import os
print (os.getenv('PYTHONPATH'))
import data_reader as dr
from dmi_open_data import  Parameter
import matplotlib.pyplot as plt
import utils
from pathlib import Path



def _usage(exitcode=0):
    """_summary_

    :param i: _description_, defaults to 4
    :type i: int, optional
    :return: _description_
    :rtype: _type_
    """    
    print('Here follows help explanation') 
    rc = exitcode
    if exitcode > 0:   
        sys.exit(exitcode)
    return rc



def main(argv):
    """
    Main program for HFP 

    Parameters
    ----------
    argv : TYPE
        Command line parameters. Run python -m hfp --help to see paramters

    Returns
    -------
    None.

    """
    
    try:
        opts, args = getopt.getopt(argv, "f:t:", ["fromdate=","todate="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        _usage(exitcode=2)
    fd='today-40' 
    td = 'today-10'

    for o, a in opts:
        if o in ("-f", "--fromdate"):
            fd = a
        elif o in ("-t", "--todate"):
            td = a
        else:
            assert False, "unhandled option"
    try:
        fd=utils.parse_date_txt(fd)
        td=utils.parse_date_txt(td)
        data_reader=dr.DataReader()
        df_energinet, df_energinet_properties = data_reader.production_data(from_date=fd, 
                                to_date=td, 
                                price_area='DK2')

        df_stations = data_reader.dmi_stations(only_dmi=True, parameter='wind_speed')


        df_observations=pd.DataFrame()
        for idx, dmi_station in df_stations.iterrows():
            print(dmi_station['properties.name'],flush=True)
            df_ = data_reader.dmi_observations(from_date=fd,to_date=td, 
                station_id=dmi_station['properties.stationId'],
                station_name=dmi_station['properties.name'],
                parameter=Parameter.WindSpeed)
            if df_ is not None: 
                df_observations=pd.concat([df_observations,df_[['fromDatetime','value','station_name','station_id']]])

        df_stat=df_energinet.query(''' property=='OnshoreWindGe50kW_MWh' ''').rename(columns={'value':'production'}).\
                merge(df_observations.rename(columns={'value':'wind_speed'}), on='fromDatetime')
        df_corr=df_stat.groupby(['station_name'])[['production','wind_speed']].corr().reset_index().query(''' level_1 == 'production' ''').sort_values('wind_speed').reset_index()

        df_corr.to_excel('test/correlations.xlsx')
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
    except (Exception) as error:
        raise error
    

if Path(sys.argv[0]).name == "sphinx-build" or Path(sys.argv[0]).name == "build.py":
    main(None)
else:
    main(sys.argv[1:])


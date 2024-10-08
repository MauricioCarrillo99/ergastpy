# -*- coding: utf-8 -*-

# **Library**
"""

import erpy2set.unravel as un
import requests as r
import json 
import pandas as pd
import numpy as np

"""# **QUERY PACK**


"""

########################################
#####   retrieve laps table  ####### v1.1
########################################

def laps_tbl(year):

  data=pd.DataFrame()
  n=num_races(year)

  for j in range(1,n+1):
    k=max_laps(year,j)
    
    for i in range(1,k+1):
        try:
            url=f'http://ergast.com/api/f1/{year}/{j}/laps/{i}.json'
            aux_data=pd.DataFrame(r.get(url).json()['MRData']['RaceTable']['Races'][0]['Laps'][0]['Timings'])
            aux_data[['lap','raceId']]=[i,j]
            data=pd.concat([data,aux_data],axis=0)
        except:
            i+=1
  return data

########################################
#### retrieve pitstops table  #### v1.1
########################################

def pitstops_tbl(year):

  data=pd.DataFrame()
  n=num_races(year)

  for i in range(1,n+1):

    try:
      url=f'http://ergast.com/api/f1/{year}/{i}/pitstops.json'
      aux_data=pd.DataFrame(r.get(url).json()['MRData']['RaceTable']['Races'][0]['PitStops'])
      aux_data['raceId']=i
      data=pd.concat([data,aux_data],axis=0)
    except:
      i+=1
  return data

########################################
# retrieve constructorResults table  v1.1
########################################

def constructorResults_tbl(year):

  data=pd.DataFrame()
  n=num_races(year)

  for i in range(1,n+1):

      url=f'https://ergast.com/api/f1/{year}/{i}/results.json'

      aux_data=pd.DataFrame(r.get(url).json()['MRData']['RaceTable']['Races'][0]['Results'])
      aux_data=aux_data[['Constructor','points','status']]
      un.unravel(aux_data)

      aux_data['raceId']=i
      data=pd.concat([data,aux_data],axis=0)

  return data

########################################
#calculate the total number of laps in a race  v1.1
########################################

def max_laps(year,number_race):

  url=f'https://ergast.com/api/f1/{year}/{number_race}/results.json'
  data=r.get(url).json()
  rslts=pd.DataFrame(data['MRData']['RaceTable']['Races'][0]['Results'])['laps'].astype(int)
  
  return max(rslts)

############################################
#calculate the total number of races by season  v1.1
############################################

def num_races(year):
  races=pd.DataFrame()

  url=f'https://ergast.com/api/f1/{year}/races.json'
  data=r.get(url).json()
  races=pd.DataFrame(data['MRData']['RaceTable']['Races'])
    
  if year==2022:
    return len(races.axes[0])+1
  else:
    return len(races.axes[0])

############################################
# Return the string that contains a uppercase 
# letter at the beggining  v1.1
############################################

def firstCap(string_toCap):
  cap=string_toCap[0].capitalize()

  adj_string=cap+string_toCap[1:]

  return adj_string

############################################
#    Fix the tables names v1.1
############################################

def adj_name(tbl_name):

  if tbl_name == 'qualifyingResults':
    return 'qualifying'
  elif tbl_name == 'sprintResults':
    return 'sprint'
  else:
    return tbl_name

############################################
#   Return the query table in Parent_child format v1.1
############################################

def raw_table(table_name,year):
  Df=pd.DataFrame()
  
  dimension_tables={'seasons':'SeasonTable','drivers':'DriverTable','constructors':'ConstructorTable','circuits':'CircuitTable','status':'StatusTable','races':'RaceTable'}
  fact_tables={'driverStandings':['StandingsTable','StandingsLists'],'results':['RaceTable','Races'],'qualifyingResults':['RaceTable','Races'],'constructorStandings':['StandingsTable','StandingsLists'],'sprintResults':['RaceTable','Races']}

  depend_races=['pitstops','laps']
  depend_results=['constructorResults']

  total_races=num_races(year)
  tbl_names= list({**fact_tables,**dimension_tables})+depend_races+depend_results

  if table_name in tbl_names:
    
    
    if table_name in dimension_tables:

     url=f'https://ergast.com/api/f1/{year}/{adj_name(table_name)}.json'
     data=r.get(url).json() 

     locations=dimension_tables[table_name]
     Df=pd.DataFrame(data['MRData'][locations][firstCap(table_name)])

     un.unravel(Df)

    elif table_name in fact_tables:

      for i in range(1,total_races+1):
        try:
           url=f'https://ergast.com/api/f1/{year}/{i}/{adj_name(table_name)}.json'
           data=r.get(url).json() 

           locations=fact_tables[table_name]
           aux_Df=pd.DataFrame(data['MRData'][locations[0]][locations[1]][0][firstCap(table_name)])
           un.unravel(aux_Df)
           aux_Df['racesId']=i
           aux_Df['year']=year
        
           Df=pd.concat([Df,aux_Df],axis=0)
        except:
           i+=1

    elif table_name in depend_races:

      if table_name =='pitstops':
           Df=pitstops_tbl(year)

      else:
           Df=laps_tbl(year)
      
    else:
     Df=constructorResults_tbl(year)
   
  else:
     print(f"{table_name} not found in the schema")

  return Df

############################################
#  Return the query table according to the schema 
# defined by Ergast APi v1.1
############################################

def clean_table(table_name,year):

  r_table=raw_table(table_name,year)
  try:
    if table_name=='races':

        table=r_table[['season','round','Circuit_circuitId','raceName','Circuit_circuitName','date','time','url','FirstPractice_date','SecondPractice_date','ThirdPractice_date','Sprint_date']]
        table.columns=['season','round','circuitId','raceName','circuitName','date','time','url','FirstPractice_date','SecondPractice_date','ThirdPractice_date','Sprint_date']
        return table
        
    elif table_name=='results': 

         table=r_table[['racesId','year','Driver_driverId','Constructor_constructorId','number','grid','position','positionText','points','laps','Time_time','Time_millis','FastestLap_lap','FastestLap_rank','FastestLap_Time_time','FastestLap_AverageSpeed_speed','status']]
         table.columns=['raceId','season','driverId','constructorId','number','grid','position','positionText','points','laps','time','milliseconds','fastestLap','rank','fastestLapTime','fastestLapSpeed','status']
         return table
            
    elif table_name=='circuits':

         table=r_table[['circuitId','circuitName','Location_locality','Location_country','Location_lat','Location_long','url']]
         table.columns=['circuitId','circuitName','locality','country','lat','long','url']
         return table

    elif table_name=='constructorStandings':

         table=r_table[['racesId','Constructor_constructorId','points','position','positionText','wins']]
         table.columns=['raceId','constructorId','points','position','positionText','wins']
         return table
  
    elif table_name=='driverStandings':
     
         table=r_table[['racesId','Driver_driverId','points','position','positionText','wins']]
         table.columns=['raceId','driverId','points','position','positionText','wins']
         return table

    elif table_name=='qualifyingResults':

         table=r_table[['racesId','Driver_driverId','Constructor_constructorId','number','position','Q1','Q2','Q3']]
         table.columns=['raceId','driverId','constructorId','number','position','Q1','Q2','Q3']
         return table
    
    elif table_name=='sprintResults':
    
         table=r_table[['racesId','Driver_driverId','Constructor_constructorId','number','grid','position',
               'positionText','points','laps','Time_time','Time_millis','FastestLap_lap',
               'FastestLap_Time_time', 'status']]
         table.columns=['raceId','driverId','constructorId','number','grid','position',
               'positionText','points','laps','time','millis','fastestLap',
               'fastestLaptime','status']  
         return table
    else:
         return r_table
  except:
    return r_table
  

############################################
#  Return the query table between a range of dates v1.1
############################################

def query_range(table_name,initial_date,final_date):

  Df=pd.DataFrame()

  for i in range(initial_date,final_date+1):

      aux_Df=clean_table(table_name,i)
      Df=pd.concat([DF,aux_Df],axis=0)

  

  return Df

############################################
#  Return the whole schema according to Ergast API
#  between a range of dates1.1
############################################

def full_schema(initial_date,final_date):
  tables=[]
  Df=pd.DataFrame()

  schema=['seasons','drivers','constructors','circuits','status','races','results','qualifyingResults','constructorResults','constructorStandings','driverStandings','pitstops','laps']

  for table in schema:

      Df=query_range(table,initial_date,final_date)
      tables.append(Df)
      print(f"table {table} is ready")

  print('full success at retrieving the schema')

  return dict(zip(schema, tables))

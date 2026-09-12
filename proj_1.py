import streamlit as st 
import pandas as pd
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

##deriving data
Earthquake_records =[]
start_year = datetime.now().year - 5
end_year = datetime.now().year
url = "https://earthquake.usgs.gov/fdsnws/event/1/query" 
 
 
 
Earthquake_records = [] 
for year in range(start_year, end_year+ 1): 
  for month in range(1,13): 
    start_date = f"{year}-{month:02d}-01" 
    if month == 12: 
      end_date = f"{year+1}-01-01" 
    else: 
      end_date= f"{year}-{month+1:02d}-01" 
    params = {"format" : "geojson", 
            "starttime": start_date, 
            "endtime": end_date, 
            "minmagnitude" : 3} 
 
    response = requests.get(url, params=params) 
    if response.status_code != 200: 
      print(f"failed for {start_date} : {response.text[:200]}") 
      continue 
 
    try: 
      data = response.json() 
    except Exception as e: 
        print(f"json error for {start_date} : {e}") 
        continue 
 
    for l in data["features"]: 
      p = l["properties"] 
      g = l["geometry"]["coordinates"] 
      Earthquake_records.append({ 
          "id" : l.get("id"), 
          "time" : pd.to_datetime(p.get("time"),unit = "ms"), 
          "updated" : pd.to_datetime(p.get("updated"),unit = "ms"), 
          "latitude" : g[1] if g else None, 
          "longitude" : g[0] if g else None, 
          "depth_km" :g[2] if g else None, 
          "mag" : p.get("mag"), 
          "magType" : p.get("magType"), 
          "place" : p.get("place"), 
          "status" : p.get("status"), 
          "tsunami" : p.get("tsunami"), 
          "alert" : p.get("alert"), 
          "felt" : p.get("felt"), 
          "cdi" : p.get("cdi"), 
          "mmi" : p.get("mmi"), 
          "sig" : p.get("sig"), 
          "net" : p.get("net"), 
          "code" : p.get("code"), 
          "ids" : p.get("ids"), 
          "sources" : p.get("sources"), 
          "types" : p.get("types"), 
          "nst" : p.get("nst"), 
          "dmin" : p.get("dmin"), 
          "rms" : p.get("rms"), 
          "gap" : p.get("gap"), 
          "type" : p.get("type"), 
      }) 

print(len(Earthquake_records)) 

df = pd.DataFrame(Earthquake_records) 

print(df) 

df.head() 

#data cleaning 
df["country"] = df["place"].str.split(",").str[-1].str.strip() 

df_cat_column=["magType","status","type","net","sources","types"] 

for cat in df_cat_column: 
    df[cat] = df[cat].str.strip().str.lower() 

df.isnull().sum() 

#filling null value  
df["alert"] = df["alert"].fillna("green") 
df["felt"] = df["felt"].fillna(df["felt"].median()) 
df["gap"] = df["gap"].fillna(df["gap"].median()) 
df["mmi"] = df["mmi"].fillna(df["mmi"].mean()) 
df["dmin"] = df["dmin"].fillna(df["dmin"].median()) 
df["cdi"] = df["cdi"].fillna(df["cdi"].mean()) 
df["nst"] = df["nst"].fillna(df["nst"].median()) 
df["rms"] = df["rms"].fillna(df["rms"].mean()) 
 
#derive new column with existing column
df["years"] = df["time"].dt.year 
df["months"] = df["time"].dt.month 
df["days"] = df["time"].dt.day 
df["day_of_week"] = df["time"].dt.day_name() 

df["depth_flag"] = df["depth_km"].apply( 
    lambda x: "shallow" if x < 50 else "deep" 
) 
 
#connecting mysql 
from config import DB_USER, DB_PASS, DB_HOST, DB_NAME
from sqlalchemy import create_engine

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
)
df.to_sql( 
    "earthquakes", 
    con=engine, 
    if_exists="replace", 
    index=False 
)
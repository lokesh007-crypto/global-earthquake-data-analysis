import streamlit as st 
import pandas as pd
#connecting mysql 
from config import DB_USER, DB_PASS, DB_HOST, DB_NAME
from sqlalchemy import create_engine
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
)
#sql queries
queries = {
    "0. Show tabel" : 
    """ SELECT * FROM earthquake_proj.earthquakes;
      """,
    "1. Top 10 strongest earthquakes" :
    """ select * from earthquakes
      where type ="earthquake" order by mag desc limit 10;
    """,
    "2. Top 10 deepest earthquakes" :
    """select * from earthquakes 
    where type = "earthquake" order by depth_km desc limit 10;
    """,
    "3. Earthquakes between less than 50km and more than 7.5 magnitude" :
    """select * from earthquakes 
    where depth_km < 50 and mag > 7.5 and type = "earthquake";
    """,
    "4. Average mag as per magnitude type" :
    """select magType,round(avg(mag),3) as avg_mag
      from earthquakes group by magtype;
    """,
    "5. Year with most earthquakes" :
    """select years , count(*) as earthquakes_count from earthquakes 
    group by years order by earthquakes_count desc ;
    """,
    "6. Month with highest number of earthquakes" :
    """select months , count(*) as earthquakes_count from earthquakes
      group by months order by earthquakes_count desc;
    """,
    "7. Day of week with most earthquakes" :
    """select day_of_week ,
      count(*) as earthquakes_count from earthquakes 
      group by day_of_week order by earthquakes_count desc;
    """,
    "8. Earthquakes per hour" :
    """select hour(time) as hours , count(*) as earthquakes_dayscounts from earthquakes  group by hours order by earthquakes_dayscounts;
    """,
    "9. Most active network" :
    """select net as network , count(*) as net_count from earthquakes group by net order by net_count desc;
    """,
    "10. Top 5 places with high casualities" :
    """select country,count(felt) as casualties from earthquakes group by country order by casualties desc limit;
    """,
    "11. Average economic loss by alert level" :
    """SELECT alert, COUNT(*) AS count
        FROM earthquakes
        GROUP BY alert;""",
    "12. Number of reviewed and automatic earthquakes" :
    """select status ,count(status) as status_count from earthquakes group by status;
    """,
    "13. Number of times each earthquake type occurred." :
    """select type , count(type) as type_count from earthquakes group by type;
    """,
    "14. Number of earthquakes by datatypes" :
    """select  types as d_types ,count(types) as d_types_count from earthquakes group by types ;
    """,
    "15 . Event with high station coverage" :
    """SELECT
    id,
    place,
    nst
    FROM earthquakes
    WHERE nst > 50
    ORDER BY nst DESC;""",
    "16. Number tsunami triggered per year" :
    """select years , count(tsunami) as tsunami_count from earthquakes where tsunami=1 group by years; 
    """,
    "17. Number of Earthquakes by per alert level" :
    """select alert , count(alert) as earthquake_count from earthquakes group by alert;
    """,
    "18. Top 5 countries with highest avg magnitude in past 5 years" :
    """select country , round(avg(mag),3) as avg_number from earthquakes group by country order by avg_number desc;
    """,
    "19 .Countries with both shallow and deep earthquakes in same month " :
    """select country ,years, months  from earthquakes group by country , years , months having sum(depth_flag="shallow")>0 and sum(depth_flag = "deep")>0;
    """,
    "20. Year over year growth rate in total earthquakes" :
    """with yearly_count as( select years , count(*) as earthquake_counts from earthquakes group by years)select years,earthquake_counts,lag(earthquake_counts) over (order by years) AS previous_year_count,round((earthquake_counts - lag(earthquake_counts) over (order by years))/lag(earthquake_counts) over (order by years)*100,2) as year_growth_rate from yearly_count order by years;
    """,
    "21. Top 3 seismical activity region" :
    """select place, count(*) as earthquake_count , round(avg(mag),2) as avg_mag from earthquakes group by place order by earthquake_count desc,avg_mag desc limit 3;
    """,
    "22. Average depth per country between -5 to +5 lattitude of equator" :
    """select country,round(avg(depth_km),3) as avg_depth from earthquakes where latitude between -5 and +5 group by country ;
    """,
    "23. Country with high shallow and deep earthquake ratio" :
    """select country ,sum(depth_flag = "shallow") as shallow_count , sum(depth_flag = "deep") as deep_count,round(sum(depth_flag = "shallow")/sum(depth_flag = "deep"),2) as deep_ratio from earthquakes group by country order by deep_ratio desc;
    """,
    "24. Average magnitude differance of tsunami occured and tsunami not occured " :
    """select round(avg(case when tsunami =1 then mag end),2)	 as tsunami_mag , round(avg(case when tsunami =0 then mag end),2) as non_tsunami_mag , round(avg(case when tsunami = 1 then mag end) - avg(case when tsunami = 0 then mag end),2) as tsunami_avg_diff from earthquakes;
    """,
    "25. Events with lowest data reliability using gap and rms" :
    """select country , gap ,rms from earthquakes order by rms desc,gap desc;
    """,
    "26. Region with highest frequency of deepth more than 300km" :
    """select place , depth_km from earthquakes where depth_km > 300 order by depth_km desc;
    """



}

 
#creating streamlit dashboard 
 
st.title("Earthquake data analysis dashbord") 
st.write("Select any problem statement to run the query") 
task = st.selectbox("choose task number",list(queries.keys())) 

if st.button("Run query"): 
    query = queries[task] 
    df = pd.read_sql(query,engine) 
    st.subheader(f"result for task: {task}") 
    st.dataframe(df,use_container_width=True)

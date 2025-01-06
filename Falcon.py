import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import re

#read in the data, clean it us
focal= pd.read_csv('Z:/Adi_Job/focal_systems_data.csv', delimiter=',')
                
focal.timestamp=focal.timestamp.astype('datetime64[ns]')
focal.out_of_stock_start=focal.out_of_stock_start.astype('datetime64[ns]')
focal.out_of_stock_end=focal.out_of_stock_end.astype('datetime64[ns]')
focal.date=focal.date.astype('datetime64[ns]')

def clean_and_convert_to_float(s):
    if s is None or s == "":
        return float('nan')  # Handle None or empty string as NaN
    # Use regex to keep only digits and the decimal point, removing spaces
    cleaned_str = re.sub(r'[^0-9.]', '', s)
    try:
        return float(cleaned_str) if cleaned_str else float('nan')
    except ValueError:
        return float('nan')  # Return NaN if conversion fails

focal['sales_per_hour'] = focal['sales_per_hour'].apply(clean_and_convert_to_float)
focal['expected_lost_sales'] = focal['expected_lost_sales'].apply(clean_and_convert_to_float)
focal['recouped_sales'] = focal['recouped_sales'].apply(clean_and_convert_to_float)
focal['expected_workable_lost_sales'] = focal['expected_workable_lost_sales'].apply(clean_and_convert_to_float)


#########  creation of a few additional variable #############

#create a lost sales variable
focal['lost_sales']=focal['expected_lost_sales'] - focal['recouped_sales']

#create workable flag variable
focal['Workableflag']=''
focal.loc[(focal['workable'] == False), 'Workableflag'] = 'Not Workable'
focal.loc[(focal['workable'] == True) & (focal['worked'] == False), 'Workableflag'] = 'Workable-NotWorked'
focal.loc[(focal['workable'] == True) & (focal['worked'] == True), 'Workableflag'] = 'Workable-Worked'

#create day of week variable
focal['day_of_week'] = focal['date'].dt.day_name()

#create hour of day and time of day flag
focal['hour_of_day'] = focal['timestamp'].dt.hour #create hour and time of day flag

def determine_time(hour_of_day):
    if 0<hour_of_day <10:
        return '1-Early Morning'
    elif 10 <= hour_of_day < 12:
        return '2-Mid Morning'
    elif 12 <= hour_of_day < 14:
        return '3-Mid Day'
    elif 14 <= hour_of_day < 17:
        return '4-AfterNoon'
    elif 17 <= hour_of_day < 19:
        return '5-Early Evening'
    elif 19 <= hour_of_day < 22:
        return '6-Night'
    elif hour_of_day >= 22:
        return '7-Late Night'
    else:
        return 'Unknown'
       
focal['time_of_day'] = focal['hour_of_day'].apply(determine_time)
 
#create a categories for duration of OOS
def determine_duration(out_of_stock_duration):
    if 0<out_of_stock_duration <3:
        return '1-under <3'
    elif 3 <= out_of_stock_duration < 5:
        return '2-3 to <5'
    elif 5 <= out_of_stock_duration < 7:
        return '3-5 to <7'
    elif 7 <= out_of_stock_duration < 10:
        return '4-7 to <10'
    elif 10 <= out_of_stock_duration < 15:
        return '5-10 to <15'
    elif out_of_stock_duration >= 15:
        return '7- >15'
    else:
        return 'Unknown'
       
focal['duration'] = focal['out_of_stock_duration'].apply(determine_duration)


#################### Frequencies and Summaries #####################

worksum = focal['Workableflag'].value_counts().sort_index()  #frequency of workable flag
worksum.to_csv('Z:/Adi_Job/worksum.csv')

daysum = focal['day_of_week'].value_counts().sort_index()  #frequency of OOS events by day of week
print(daysum)
daysum.to_csv('Z:/Adi_Job/daysum.csv')

timesum = focal['time_of_day'].value_counts().sort_index()  #frequency of OOS events by time of day
print(timesum)
timesum.to_csv('Z:/Adi_Job/timesum.csv')

summary_work_day = focal.groupby(['Workableflag','day_of_week']).size().reset_index(name='frequency') #freq of OOS events by workflag and day of week
summary_work_day.to_csv('Z:/Adi_Job/summary_work_day.csv', index=False)

summary_work_time = focal.groupby(['Workableflag','time_of_day']).size().reset_index(name='frequency') #freq of OOS events by workflag and time of day
summary_work_time.to_csv('Z:/Adi_Job/summary_work_time.csv', index=False)

summary_work_duration = focal.groupby(['duration','Workableflag']).size().reset_index(name='frequency') #freq of duration by workflagd
summary_work_duration.to_csv('Z:/Adi_Job/summary_work_duration.csv', index=False)

numeric_cols = focal.select_dtypes(include='number').columns
summary_df2 = focal.groupby('Workableflag')[numeric_cols].sum().reset_index() #sum of all numeric columns by workflag
summary_df2.to_csv('Z:/Adi_Job/summary_output4.csv', index=False)

summary_df2 = focal.groupby('Workableflag','DSD')[numeric_cols].sum().reset_index() #sum of all numeric columns by workflag
summary_df2.to_csv('Z:/Adi_Job/summary_workflag_dsd.csv', index=False)


quit()

#print(focal.head(10000))
#print (focal.dtypes)
#print(df['sales_per_hour'].sum())
#print(df.describe().to_string())
#print(df.shape)
#print(focal.info(verbose=True))

#for index, row in df.iterrows():
#    if row['workable']==True and row['DSD']==True:
#       df.loc[index,'flag']='dud'

#dtype={'timestamp':'str','date':'str','UPC':'str','DSD':'bool',
#'workable':'bool','worked':'bool','out_of_stock_start':'str','out_of_stock_end':'str',
#'out_of_stock_duration':'float', 'expected_out_of_stock_duration':'float',
#'hours_recouped':'float','sales_per_hour':'float', 'expected_lost_sales':'float',
#'expected_workable_lost_sales':'float','recouped_sales':'float'})
#converters={'sales_per_hour':lambda x : float(x.strip("$ $- '' ' ' ")),
#'expected_lost_sales':lambda x : float(x.strip("$ $- '' ' ' ")),
#'recouped_sales':lambda x : float((x.strip("$ $- ( ) '' ' ' ")).replace('','0')),
#'expected_workable_lost_sales':lambda x : float((x.strip("$ $- ( ) '' ' ' ")).replace('','0'))})



# -*- coding: utf-8 -*-
import datetime
import  numpy as np, pandas as pd, matplotlib.pyplot as plt
import ast, os
import urllib2
from bs4 import BeautifulSoup
import json
import zipfile
import matplotlib as mpl
import gmplot




# given an url, get list of holidays
def getHolidays (url):
    page=urllib2.urlopen(url)
    soup=BeautifulSoup(page, 'html.parser')
    holidays=[]
    out=soup.findAll('div',attrs={'class':'col-md-3 black-link'})
    for i in out:
        holidays.append(str(i.text))

    return holidays

# flag as 1 the non-working days (public holidays of weekends)
def flagHolidays(x):
    # if it's saturday or sunday, it's automatically a "holiday"
    if datetime.datetime.isoweekday(x)==6 or  datetime.datetime.isoweekday(x)==7:
        return 1
    
    # otherwise, check if it's a public holiday
    if x in holidays:
        return 1
    else:
        return 0


# getting public holidays for 2013 and 2014
url_2013='https://www.feiertagskalender.ch/index.php?geo=3516&jahr=2013&hl=en'
url_2014='https://www.feiertagskalender.ch/index.php?geo=3516&jahr=2014&hl=en'

holidays=getHolidays(url_2013)
holidays+=getHolidays(url_2014)


# converting into the same date format as the original dataset
temp=[]
for date in holidays:
    day=datetime.datetime.date(datetime.datetime.strptime(date, '%B %d %Y'))
    temp.append(day)
holidays=temp



def calc_duration(x):
    return (len(x)-1)*15

def get_hour(x):
    return int(str(x)[-8:-6])

def round_coordinates(x):
 #   x=np.asarray(x)
    decimals=3
    # iterating over all the points
    for i in range(len(x)):
    # for each point, rounding both x and y coordinates
        x[i][0]=round(x[i][0],decimals)
        x[i][1]=round(x[i][1],decimals)

    return x



def to_binary(x):
    x=str(x)
    if x=='False':
        return 0
    elif x=='True':
        return 1
    else:
        # flag for error
        return -1

def start(x):
    return x[0]
def end(x):
    return x[-1]



##def bin_hour_of_day(hour):
##    #initializing variables
##    
##    if hour>6 and hour <=10:
##        return 1
##    elif hour>10 and hour <=11:
##        return 2
##    elif hour>11 and hour <=12:
##        return 3
##    elif hour>12 and hour <=14:
##        return 4
##    elif hour>14 and hour <=16:
##        return 5
##    elif hour>16 and hour <=18:
##        return 6
##    elif hour>18 and hour <=22:
##        return 7
##    elif hour>22 and hour <=24:
##        return 8
##    elif hour>0 and hour <=6:
##        return 9
##    else:
##        return 9


   
def bin_hour_of_day(x):
#    print (x)
#    print (x[0])
#    print (x[1])
#    print (x)
    holiday=x['holiday']
    hour=x['hour']


    # bin for holidays
    if holiday==1:
        return 4

    if hour>6 and hour <=10:
        return 1
    elif hour>10 and  hour <=16:
        return 2
    elif hour >16 and hour <=20:
        return 1
    else:
        return 3

def start_same_end(x):
    if x[0]==x[-1]:
        return 1
    return 0


def lookup(x):
    holiday=x['holiday']
    hour=x['hour']


#df = pd.read_csv('train.csv')
#df = df.sample(frac=0.001)

## to load the entire dataset and then save a sample of it
#df = pd.read_csv('C:/Users/chiar/Documents/Heavy files/494 python project/train.csv')
#df = df.sample(frac=0.1)
#df.to_csv('C:/Users/chiar/Documents/Heavy files/494 python project/train_sampled.csv', sep=',')


# to load the sample
#df = pd.read_csv('Porto_taxi_data_test_partial_trajectories.csv')
df = pd.read_csv('train_sampled.csv')

#df = pd.read_csv('test.csv')


# to load the entire dataset
#df = pd.read_csv('train.csv')

# to load a
#df = pd.read_csv('a.csv')


#print df


# initializing new columns to populate later
df['duration'] = np.zeros(len(df))
df['date'] = np.zeros(len(df))
df['hour'] = np.zeros(len(df))
df['datetime'] = np.zeros(len(df))
df['route'] = np.zeros(len(df))
df['route_string'] = np.zeros(len(df))
df['start'] = np.empty((len(df), 0)).tolist()
df['end'] =  np.empty((len(df), 0)).tolist()
df['holiday'] = np.zeros(len(df))
df['start_same_end'] = np.zeros(len(df))



# converting timestamp into date and hour
df['datetime'] = df['TIMESTAMP'].apply(datetime.datetime.fromtimestamp)
df['date'] = df['TIMESTAMP'].apply(datetime.date.fromtimestamp)
df['hour'] = df['datetime'].apply(get_hour)
# removing helper column
df.drop('datetime', axis=1, inplace=True)

print type(date)
'''
# flagging holidays
df['holiday'] = df['date'].apply(flagHolidays)

# removing all the non-holiday days
#df.drop(df[df['holiday'] ==0].index, inplace=True)


# converting missing colum into 0/1
df['MISSING_DATA'] = df['MISSING_DATA'].apply(to_binary)


# removing rows with missing coordinates
df.drop(df[df['MISSING_DATA'] >0].index, inplace=True)



print("started converting polyline")
# converting polyline into an array of arrays
df['POLYLINE'] = df['POLYLINE'].apply(ast.literal_eval)


print("done converting polyline")

## removing rows with empty poliline or <=2 points
#df.drop(df[len(df['POLYLINE'])<=2].index, inplace=True)
#
df.describe()
'''
# computing duration in seconds
df['duration'] = df['POLYLINE'].apply(calc_duration)


# removing the (many) rows that have duration <0 (their POLYLINE is empty or has only one point... wrong rows?)
df.drop(df[df['duration'] <=15].index, inplace=True)
'''


### rounding coordinates
##print("started rounding coordinates")
##df['route'] = df['POLYLINE'].apply(round_coordinates)
##print("done rounding coordinates")

# rounding coordinates
##df['route'] = df['POLYLINE'].apply(round_coordinates)
##
##df['start'] = df['route'].apply(start)
##df['end'] = df['route'].apply(end)
##df['start_same_end'] = df['route'].apply(start_same_end)
##df.drop(df[df['start_same_end'] ==1].index, inplace=True)

#df['start'] = df['POLYLINE'].apply(start)
#df['end'] = df['POLYLINE'].apply(end)
#print df.start
#se = df.filter(['start','end'], axis=1)
#se.to_csv('se_a.csv')
#print df



##print df.route[0][1][1]
##
##import gpxpy.geo
##
##dist = gpxpy.geo.haversine_distance(df.route[0][1][0],df.route[0][1][1],-8.585676,41.148522)
##print(dist)

#sorting the data for plotting
##[df['hour'], df['duration']] = zip(*sorted(zip(df['hour'], df['duration']), key=lambda x: x[0]))
### creating bins for hour of the day
#print("started binning")

df['time_bin'] = np.zeros(len(df))
#df['time_bin'] = df.apply(lambda row: bin_hour_of_day(row['hour'], row['holiday']))
df['time_bin'] = df.apply(bin_hour_of_day, axis=1)
print("done binning")

# to save the dataset as obtained so far, keeping all data types and colum names
#print ("saving pickle")
#df.to_pickle('output.pkl')
#print ("done saving pickle")

#computing the average duration by hour of the day and by route (output is a separate table)

#creating helper column with route converted to string
#
##df['route_string'] = df['route'].apply(str)
##df['start'] = df['start'].apply(str)
##df['end'] = df['end'].apply(str)


#df['holiday'] = df['date'].apply(flagHolidays)
#df['holiday'].describe()
#df.head(2100)

#print df


###filtering only the hour/route pairs that have a number of occurrences above a threshold 
##min_count=2
##avgtime_byhour_byroute=df.groupby(['time_bin','route_string','holiday','start','end'],as_index=False )['duration'].agg(['mean','count'],as_index=False)
###avgtime_byhour_byroute=avgtime_byhour_byroute.drop(avgtime_byhour_byroute[avgtime_byhour_byroute['count']<min_count].index)
###avgtime_byhour_byroute.to_csv('final_random.csv')
##
##se = df.filter(['start','end'], axis=1)
##se.to_csv('se.csv')





#print df
#print avgtime_byhour_byroute
#df_dur= pd.merge(df, avgtime_byhour_byroute, on=['time_bin','route_string'])
#print df_dur
#avgtime_byhour_byroute.rename(columns={'mean': 'avgtime_byhour_byroute'}, inplace=True)
#print avgtime_byhour_byroute



##
### showing duration versus hour of the day (for then binning)
##plt.plot(df['hour'], df['duration'])
##
##plt.show()
'''

means =df.groupby('hour', as_index=False)['duration'].mean()
print means
plt.plot(means['hour'], means['duration'], '.')
plt.show()
#######################################################################################################

'''




# computing the average duration by hour of the day and by route (output is a separate table)

# creating helper column with route converted to string
#df['route_string'] = df['route'].apply(str)
# filtering only the hour/route pairs that have a number of occurrences above a threshold 
##min_count=2
##avgtime_byhour_byroute=df.groupby(['hour', 'route_string'],as_index=False )['duration'].agg(['mean','count'],as_index=False)
##avgtime_byhour_byroute=avgtime_byhour_byroute.drop(avgtime_byhour_byroute[avgtime_byhour_byroute['count']<min_count].index)
##
#df_dur= pd.merge(df, avgtime_byhour_byroute, on=['hour', 'route_string'])
#avgtime_byhour_byroute.rename(columns={'mean': 'avgtime_byhour_byroute'}, inplace=True)







##################
### to save the dataset as obtained so far, keeping all data types and colum names
##df.to_pickle('output.pkl')
##
### to read back the complete file previously saved
##df=pd.read_pickle('output.pkl') 

# to see where it saved the file
#print os.getcwd()
################









#df.describe()










## PREVIOUS CODE THAT DOESN'T RUN. YOU CAN DE-BUG IT AND PUT IT TO WORK AGAIN IF YOU WANT
##
######df = pd.read_csv('Porto_taxi_data_test_partial_trajectories.csv')
##df["duration"] = np.nan
##df["hour"] = np.nan
##
##for row in df.index:
##    test = df.POLYLINE[row].split(",")
##    df.duration[row] = float(len(test)*15/2)
##    df.TIMESTAMP[row] = datetime.datetime.fromtimestamp(int(df.TIMESTAMP[row])).strftime('%Y-%m-%d %H:%M:%S')
##    df.hour[row] = df.TIMESTAMP[row][11:13]
##print df[:100]
##
##mean = np.mean(df.duration, axis=0)
##sd = np.std(df.duration, axis=0)
##upper = mean + 2 * sd
##lower = mean - 2 * sd
##
##for row in df.index:
##    if df.duration[row] > upper or df.duration[row] < lower:
##        df.drop(row, inplace=True)
##    else:
##        continue
##print "here"
##print df[:100]
##    
##plt.scatter(df['hour'],df['duration'])
##plt.show()

'''

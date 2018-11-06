import datetime
import  numpy as np, pandas as pd, matplotlib.pyplot as plt
import ast, os
import urllib2
from bs4 import BeautifulSoup
import json
import zipfile
import matplotlib as mpl
import psycopg2
import gmplot

def start(x):
    return x[0]
def end(x):
    return x[-1]


df = pd.read_csv('se_big.csv')


df['start'] = np.empty((len(df), 0)).tolist()
df['end'] =  np.empty((len(df), 0)).tolist()

df['POLYLINE'] = df['POLYLINE'].apply(ast.literal_eval)

 
    

df['start'] = df['POLYLINE'].apply(start)
df['end'] = df['POLYLINE'].apply(end)
se = df.filter(['start','end'], axis=1)
se.to_csv('se_big.csv')
df.drop('POLYLINE', axis=1, inplace=True)

pol_original = [[-8.61084, 41.145714], [-8.61084, 41.145705], [-8.610858, 41.145714], [-8.610561, 41.146092], [-8.609607, 41.146722], [-8.608788, 41.147208], [-8.609445, 41.147568], [-8.610228, 41.147586], [-8.610264, 41.147757], [-8.610291, 41.147811], [-8.611218, 41.147937], [-8.612118, 41.148063], [-8.613819, 41.148423], [-8.614287, 41.148342], [-8.614638, 41.147721], [-8.615412, 41.147289], [-8.616618, 41.147244], [-8.617689, 41.147235], [-8.617734, 41.147208], [-8.617959, 41.147208], [-8.617995, 41.147226], [-8.617986, 41.147343], [-8.618265, 41.148459], [-8.619102, 41.148693], [-8.619669, 41.148279], [-8.619741, 41.148207], [-8.620038, 41.14782], [-8.620407, 41.147433], [-8.620416, 41.147424], [-8.621181, 41.14746], [-8.621388, 41.147487], [-8.621469, 41.147469], [-8.621856, 41.147559], [-8.622198, 41.147613], [-8.622306, 41.147442], [-8.622315, 41.147442], [-8.622324, 41.147424], [-8.622333, 41.147433], [-8.622369, 41.147397], [-8.622423, 41.147172], [-8.622441, 41.147154]]
pol1_predicted = [[-8.61084, 41.145714], [-8.61084, 41.145705], [-8.610858, 41.145714], [-8.610561, 41.146092], [-8.609607, 41.146722], [-8.608788, 41.147208], [-8.609445, 41.147568], [-8.610228, 41.147586], [-8.610264, 41.147757], [-8.610291, 41.147811], [-8.611218, 41.147937], [-8.612118, 41.148063], [-8.613819, 41.148423], [-8.614287, 41.148342], [-8.614638, 41.147721], [-8.615412, 41.147289], [-8.616618, 41.147244], [-8.617689, 41.147235], [-8.617734, 41.147208], [-8.617959, 41.147208], [-8.617995, 41.147226], [-8.617986, 41.147343], [-8.618265, 41.148459], [-8.619102, 41.148693], [-8.619669, 41.148279], [-8.619741, 41.148207], [-8.620038, 41.14782], [-8.620407, 41.147433], [-8.620416, 41.147424], [-8.621181, 41.14746], [-8.621388, 41.147487], [-8.621469, 41.147469], [-8.621856, 41.147559], [-8.622198, 41.147613], [-8.622306, 41.147442], [-8.622315, 41.147442], [-8.622324, 41.147424], [-8.622333, 41.147433], [-8.622369, 41.147397], [-8.622423, 41.147172], [-8.622441, 41.147154]]
pol2_original = [[-8.644383, 41.175351], [-8.644842, 41.175864], [-8.644131, 41.17689], [-8.64252, 41.177871], [-8.641278, 41.177232], [-8.640477, 41.177619], [-8.639928, 41.178375], [-8.638983, 41.178933], [-8.638146, 41.178888], [-8.638146, 41.178699], [-8.638173, 41.178483], [-8.638173, 41.178438], [-8.638182, 41.17851]]
pol2_predicted = [[-8.64432, 41.175486], [-8.645031, 41.176053], [-8.643798, 41.176998], [-8.641998, 41.177745], [-8.6409, 41.177169], [-8.640333, 41.177907], [-8.639289, 41.178726], [-8.638146, 41.178879], [-8.638164, 41.178501]]
lat = list()
lon = list()
for i in range(len(pol)):
    lat.append(pol[i][0])
    lon.append(pol[i][1])

lat1 = list()
lon1 = list()
for i in range(len(pol1)):
    lat1.append(pol1[i][0])
    lon1.append(pol1[i][1])
    

df['start_lat'], df['start_long'] = df['start'].str.split(',', 1).str
df['end_lat'], df['end_long'] = df['end'].str.split(',', 1).str

print df


df.start_lat = df.start_lat.str.strip('[')
df.start_long = df.start_long.str.strip(']')
df.end_lat = df.end_lat.str.strip('[')
df.end_long = df.end_long.str.strip(']')
df.start_lat = df.start_lat.astype(float)
df.start_long = df.start_long.astype(float)
df.end_lat = df.end_lat.astype(float)
df.end_long = df.end_long.astype(float)

gmap = gmplot.GoogleMapPlotter(41.1496100, -8.6109900, len(pol))

#gmap.scatter(df.start_long,df.start_lat, 'r', 100, marker=False)
#gmap.scatter(df.end_long,df.end_lat, 'b', 100, marker=False)
gmap.plot(lon,lat, 'b', 1, marker=False)
gmap.plot(lon1,lat1, 'g', 1, marker=False)
gmap.draw('map.html')
gmap.draw('map1.html')











































































##df = pd.read_csv('train.csv', 
##                 sep = ",",
##                 chunksize = 1000,
##                 iterator = True,
##                 usecols = ['POLYLINE'],
##                 converters={'POLYLINE': lambda x: json.loads(x)})
##
##lat_mid = 41.1496100
##lon_mid = -8.6109900
##
##nrbins = 2000
##hist = np.zeros((nrbins,nrbins))
##
##for data in df:
##  # Get just the longitude and latitude coordinates for each trip
##  latlong = np.array([ coord for coords in data['POLYLINE'] for coord in coords if len(coords) > 0])
##
##  # Compute the histogram with the longitude and latitude data as a source
##  hist_new, _, _  = np.histogram2d(x = latlong[:,1], y = latlong[:,0], bins = nrbins, 
##                                   range = [[lat_mid - 0.1, lat_mid + 0.1], [lon_mid - 0.1, lon_mid + 0.1]])
##                                   
##  # Add the new counts to the previous counts
##  hist = hist + hist_new
##  
##
### We consider the counts on a logarithmic scale
##img = np.log(hist[::-1,:] + 1)
##
### Plot the counts
##plt.figure()
##ax = plt.subplot(1,1,1)
##plt.imshow(img)
##plt.axis('off')
##      
##plt.savefig('trips_density.png')

    

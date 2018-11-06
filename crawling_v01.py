import urllib2
from bs4 import BeautifulSoup

import datetime
import numpy as np
import project_code_latest as pc

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

# adding new column for the holiday flag and populating it
##pc.df['holiday'] = np.zeros(len(pc.df))
##pc.df['holiday'] = pc.df['date'].apply(flagHolidays)
###df['holiday'].describe()
##pc.df.head(2100)

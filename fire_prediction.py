
# coding: utf-8

# In[8]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random


# Read the data in, can also use dtype guessing to handle the column memory demanding
# In this case, trun the low_memory = Flase to handle
train_data=pd.read_csv("data/Incidents_Responded_to_by_Fire_Companies.csv",low_memory=False)

# train_data=train_data.drop("Id",1)
train_data.head()

print('Total number of incidents: {}'.format(len(train_data)))


# In[62]:


value = np.array(train_data['INCIDENT_TYPE_DESC'])
import collections
count = collections.Counter(value)
max_count_of_incident = list(count.most_common(1))
a = max_count_of_incident[0][1]/len(train_data)
print('The most common type of incident rate is {}'.format( a ))


# In[66]:


print('Ratio of 111-building fire to 651 - Smoke scare: {}'.format(count['111 - Building fire']/count['651 - Smoke scare, odor of smoke']))


# In[114]:


a = train_data.loc[(train_data["INCIDENT_TYPE_DESC"]=="710 - Malicious, mischievous false call, other") & (train_data["BOROUGH_DESC"]=="1 - Manhattan") , ["INCIDENT_TYPE_DESC","BOROUGH_DESC"]]
b = train_data.loc[(train_data["INCIDENT_TYPE_DESC"]=="710 - Malicious, mischievous false call, other") & (train_data["BOROUGH_DESC"]=="3 - Staten Island") , ["INCIDENT_TYPE_DESC","BOROUGH_DESC"]]
print(a.count()/b.count())


# In[121]:


train_data['INCIDENT_DATE_TIME'] = pd.to_datetime(train_data['INCIDENT_DATE_TIME'])
#pd.DatetimeIndex(train_data['INCIDENT_DATE_TIME'])


# In[124]:


train_data['ARRIVAL_DATE_TIME'] = pd.to_datetime(train_data['ARRIVAL_DATE_TIME'])


# In[128]:


train_data=pd.read_csv("data/Incidents_Responded_to_by_Fire_Companies.csv",low_memory=False)
Building_fire_start = train_data.loc[(train_data["INCIDENT_TYPE_DESC"]=="111 - Building fire") & (train_data["INCIDENT_DATE_TIME"]) , ["INCIDENT_TYPE_DESC","INCIDENT_DATE_TIME"]]
Building_fire_arrive = train_data.loc[(train_data["INCIDENT_TYPE_DESC"]=="111 - Building fire") & (train_data["ARRIVAL_DATE_TIME"]) , ["INCIDENT_TYPE_DESC","ARRIVAL_DATE_TIME"]]


# In[130]:


Building_fire_start['INCIDENT_DATE_TIME'] = pd.to_datetime(Building_fire_start['INCIDENT_DATE_TIME'])
Building_fire_arrive['ARRIVAL_DATE_TIME'] = pd.to_datetime(Building_fire_arrive['ARRIVAL_DATE_TIME'])


# In[138]:


Building_fire_arrive['Time_difference'] = Building_fire_arrive['ARRIVAL_DATE_TIME'] - Building_fire_start['INCIDENT_DATE_TIME']
Building_fire_arrive['Time_difference_second'] = Building_fire_arrive['Time_difference'].dt.total_seconds()


# In[144]:


Building_fire_arrive['Time_difference_minutes'] = Building_fire_arrive['Time_difference_second'] / 60.0
print(Building_fire_arrive['Time_difference_minutes'].quantile([0.25,0.5,0.75]))


# In[186]:


Cooking_fire_and_time = train_data[["INCIDENT_TYPE_DESC" , "INCIDENT_DATE_TIME"]]
Cooking_fire_and_time['INCIDENT_DATE_TIME'] = pd.to_datetime(Cooking_fire_and_time['INCIDENT_DATE_TIME']).dt.hour


# In[203]:


Cooking_fire_and_time
#=="113 - Cooking fire, confined to container"
a = Cooking_fire_and_time.loc[Cooking_fire_and_time['INCIDENT_TYPE_DESC'] =="113 - Cooking fire, confined to container"]
group1 = Cooking_fire_and_time.groupby('INCIDENT_DATE_TIME', as_index=False)['INCIDENT_TYPE_DESC'].count()
group1


# In[216]:


group2 = a.groupby('INCIDENT_DATE_TIME', as_index=False)['INCIDENT_TYPE_DESC'].count()
group2


# In[219]:


group3 = group2['INCIDENT_TYPE_DESC']/group1['INCIDENT_TYPE_DESC']
print('The highest cooking fire propotion is {}'.format(group3.max()))


# In[328]:


resident_zip_code =pd.read_csv("data/2010+Census+Population+By+Zipcode+(ZCTA).csv",low_memory=False)
resident_zip_code["Zip Code ZCTA"] = resident_zip_code["Zip Code ZCTA"].astype('float')
#resident_zip_code.head()
resident_zip_code = resident_zip_code.rename(columns={"Zip Code ZCTA": "ZIP_CODE"})
zip_incident = train_data.loc[(train_data["INCIDENT_TYPE_DESC"]=="111 - Building fire") & (train_data["ZIP_CODE"]) , ["INCIDENT_TYPE_DESC","ZIP_CODE"]]
zip_incident["ZIP_CODE"] = zip_incident["ZIP_CODE"].astype(float)

population_zip_fire = pd.merge(zip_incident,resident_zip_code,how='inner', on = ['ZIP_CODE'] )

count_fire_with_pop = population_zip_fire.groupby(population_zip_fire['2010 Census Population']).size().reset_index(name='Num. Building fire')
count_fire_with_pop['2010 Census Population']
#zip_incident
#population_zip_fire = train_data.loc[population_zip_fire["Zip Code ZCTA"] == population_zip_fire["ZIP_CODE"] & (population_zip_fire["2010 Census Population"]),["ZIP_CODE","2010 Census Population"]]
#population_zip_fire


# In[334]:


results = {}
coeffs = numpy.polyfit(count_fire_with_pop['2010 Census Population'],count_fire_with_pop['Num. Building fire'],2)
x = count_fire_with_pop['2010 Census Population']
y = count_fire_with_pop['Num. Building fire']
p = numpy.poly1d(coeffs)
# fit values, and mean
yhat = p(x)                         # or [p(z) for z in x]
ybar = numpy.sum(y)/len(y)          # or sum(y)/len(y)
ssreg = numpy.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
sstot = numpy.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
results['determination'] = ssreg / sstot
print(results['determination'])


# In[605]:


#CO_detector = CO_detector[np.isfinite(df['EPS'])]
CO_detector = train_data.loc[train_data["CO_DETECTOR_PRESENT_DESC"].isin(['Yes','No']) & train_data["CO_DETECTOR_PRESENT_DESC"]]
CO_detector = CO_detector[["CO_DETECTOR_PRESENT_DESC","INCIDENT_DATE_TIME","LAST_UNIT_CLEARED_DATE_TIME"]]
CO_detector['INCIDENT_DATE_TIME'] = pd.to_datetime(CO_detector['INCIDENT_DATE_TIME'])
CO_detector['LAST_UNIT_CLEARED_DATE_TIME'] = pd.to_datetime(CO_detector['LAST_UNIT_CLEARED_DATE_TIME'])


# In[607]:


CO_detector['Time_difference'] = CO_detector['LAST_UNIT_CLEARED_DATE_TIME'] - CO_detector['INCIDENT_DATE_TIME']
CO_detector['Time_difference_minutes'] = CO_detector['Time_difference'].dt.total_seconds()/60.0


# In[585]:


#time_group = CO_detector.groupby('Time_difference_minutes',np.linspace(20.0,70.0,num = 6))
#bins = [[20,30],[30,40],[40,50],[50,60],[60,70]]
bins = [20,30,40,50,60,70]
group_names = ['20-30','30-40','40-50','50-60','60-70']

CO_detector["Time_difference_minutes"] = CO_detector["Time_difference_minutes"].astype('float')
CO_detector = CO_detector.loc[CO_detector["Time_difference_minutes"]>19.9999 ]
CO_detector = CO_detector.loc[CO_detector["Time_difference_minutes"]<70.001 ]

time_group_1 = CO_detector.groupby( pd.cut(CO_detector['Time_difference_minutes'],bins,include_lowest=True) ).count()
time_group_Yes = CO_detector.loc[CO_detector["CO_DETECTOR_PRESENT_DESC"] == 'Yes' ]

time_group_Yes = time_group_Yes.groupby( pd.cut(time_group_Yes['Time_difference_minutes'],bins,include_lowest=True) ).count()
time_group_No  = CO_detector.loc[CO_detector["CO_DETECTOR_PRESENT_DESC"] == 'No']

time_group_No = time_group_No.groupby( pd.cut(time_group_No['Time_difference_minutes'],bins,include_lowest=True) ).count()
a= time_group_No['CO_DETECTOR_PRESENT_DESC']/time_group_1['CO_DETECTOR_PRESENT_DESC']

b= time_group_Yes['INCIDENT_DATE_TIME']/time_group_1['INCIDENT_DATE_TIME']
a = np.array(a)
time_group_No


# In[586]:


time_group_1 = time_group_1.rename(index=str,columns ={"CO_DETECTOR_PRESENT_DESC" : "count_total"})
time_group_1 = time_group_1["count_total"]
time_group_1 = np.array(time_group_1)


# In[587]:


time_group_Yes  = time_group_Yes.rename(index=str,columns ={"CO_DETECTOR_PRESENT_DESC" : "count_yes"})
time_group_Yes = time_group_Yes["count_yes"]
time_group_Yes = np.array(time_group_Yes)

time_group_No  = time_group_No.rename(index=str,columns ={"CO_DETECTOR_PRESENT_DESC" : "count_no"})
time_group_No = time_group_No["count_no"]
time_group_No = np.array(time_group_No)
print(time_group_Yes,time_group_No)


# In[588]:


number30 = CO_detector.loc[CO_detector["Time_difference_minutes"]==30.00 ]
number30 = number30['CO_DETECTOR_PRESENT_DESC'].count()
number40 = CO_detector.loc[CO_detector["Time_difference_minutes"]==40.00 ]
number40 = number40['CO_DETECTOR_PRESENT_DESC'].count()
number50 = CO_detector.loc[CO_detector["Time_difference_minutes"]==50.00 ]
number50 = number50['CO_DETECTOR_PRESENT_DESC'].count()
number60 = CO_detector.loc[CO_detector["Time_difference_minutes"]==60.00 ]
number60 = number60['CO_DETECTOR_PRESENT_DESC'].count()


# In[582]:


num_add = [number30,number40,number50,number60]
print(time_group_1)

for i in range(1,len(time_group_1)-1):
    time_group_1[i] += num_add[i-1]


# In[589]:


number30y = CO_detector.loc[CO_detector["Time_difference_minutes"]==30.00 ]
number30y = number30y.loc[number30y["CO_DETECTOR_PRESENT_DESC"] == 'Yes' ]
number30y = number30y['CO_DETECTOR_PRESENT_DESC'].count()

number40y = CO_detector.loc[CO_detector["Time_difference_minutes"]==40.00 ]
number40y = number40y.loc[number40y["CO_DETECTOR_PRESENT_DESC"] == 'Yes' ]
number40y = number40y['CO_DETECTOR_PRESENT_DESC'].count()

print(time_group_1)
time_group_Yes[1] += number30y
time_group_No[1] += num_add[0]-number30y

time_group_Yes[2] += number40y
time_group_No[2] += num_add[1]-number40y
print(time_group_Yes,time_group_No)


# In[592]:


ratio_yes = time_group_Yes/time_group_1
ratio_no  = time_group_No/time_group_1
print(ratio_yes,ratio_no)


# In[594]:


ratio = ratio_no/ratio_yes
print(ratio)


# In[595]:


mid_point_bins = [25,35,45,55,65]
print(mid_point_bins)


# In[597]:


p1 = numpy.polyfit (mid_point_bins,ratio,1)
result = numpy.polyval(p1,39)
print(result)


# In[602]:


#Question 6
from scipy import stats
print(time_group_1)
CO_detector = CO_detector.loc[CO_detector["Time_difference_minutes"]>60.0 ]
CO_detector


# In[619]:


CO_detector_NO = train_data.loc[train_data["CO_DETECTOR_PRESENT_DESC"].isin(['No']) & train_data["CO_DETECTOR_PRESENT_DESC"]]
CO_detector_NO = CO_detector_NO[["CO_DETECTOR_PRESENT_DESC","INCIDENT_DATE_TIME","LAST_UNIT_CLEARED_DATE_TIME"]]
CO_detector_NO['INCIDENT_DATE_TIME'] = pd.to_datetime(CO_detector_NO['INCIDENT_DATE_TIME'])
CO_detector_NO['LAST_UNIT_CLEARED_DATE_TIME'] = pd.to_datetime(CO_detector_NO['LAST_UNIT_CLEARED_DATE_TIME'])
CO_detector_NO['Time_difference'] = CO_detector_NO['LAST_UNIT_CLEARED_DATE_TIME'] - CO_detector_NO['INCIDENT_DATE_TIME']
CO_detector_NO['Time_difference_minutes'] = CO_detector_NO['Time_difference'].dt.total_seconds()/60.0


# In[623]:


small_than60 = CO_detector_NO.loc[CO_detector_NO["Time_difference_minutes"]<=60 ]
count_small60 = small_than60['CO_DETECTOR_PRESENT_DESC'].count()


print(count_small60)


# In[629]:


over_than60 = CO_detector_NO.loc[CO_detector_NO["Time_difference_minutes"]>60 ]
over_small60 = over_than60['CO_DETECTOR_PRESENT_DESC'].count()
print(over_small60)


# In[641]:


total = count_small60+ over_small60
pro1 = count_small60/total
pro2 = over_small60/total
print(pro1,pro2)


# In[642]:


from scipy.stats import chisquare
chisq, p = chisquare([pro1,pro2],ddof=1)
print(chisq)


# In[628]:





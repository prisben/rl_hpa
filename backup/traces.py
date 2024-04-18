import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import csv
import datetime
import matplotlib.dates as mdates
from statistics import mean

df1 = pd.read_csv('1fkyiupl_oneday.csv')
df1['Datetime'] = pd.to_datetime(df1["Datetime"])
df1['Datetime'] = df1['Datetime'].dt.strftime('%H:%M:%S.%f')


dfx = df1[["AnonAppName", "Datetime"]]
agg = dfx.groupby("Datetime").aggregate('count')

X = np.arange(len(dfx['Datetime'].unique()))
#plt.plot(X, agg["AnonAppName"])
#plt.xlabel("Time")
#plt.ylabel("Number of requests")
#plt.title("Number of requests over time")
#plt.show()

df2 = df1[(df1['Datetime'] < '04:03:00.000')]
print(df2)
# min timestamp 1606099970580
#max timestamp 1606103549904
df2["Count"] = ""
agg2 = df2.groupby("Timestamp").count().reset_index()
print(agg2.columns)
print(agg2)
X = np.arange(len(df2['Timestamp'].unique()))
#plt.plot(X, agg2["Count"])
#plt.xlabel("Time")
#plt.ylabel("Number of requests")
#plt.title("Number of requests over one hour")
#plt.show()


#setAllTimestamp = list(range(1606099970580, 1606103549911))
setAllTimestamp = list(range(1606100570585, 1606104170585))
def readList(path):
    list = []
    with open(path, "r") as f:
        for line in f:
            list.append(int(line.strip()))
    return list
listCount = readList("listCount.txt")
#for i in setAllTimestamp:
#    index = agg2.index[agg2['Timestamp'] == i]
#    if index.empty:
#        listCount.append(0)
#    else:
#        st = str(agg2.loc[index, 'Count']).split()[1]
#        n = int(st)
#        listCount.append(n)
#with open("listCountOld.txt", "w") as f:
#    for s in listCount:
#        f.write(str(s) + "\n")




#plt.plot(setAllTimestamp, listCount)
#plt.xlabel("Time")
#plt.ylabel("Number of requests")
#plt.title("Number of requests over one hour")
#plt.show()



new = np.add.reduceat(listCount, np.arange(0, len(listCount), 1000))


tenminuteseconds = list(range(0,3600))




plt.plot(tenminuteseconds, new)
plt.xlabel("TIME [s]", fontsize=18)
plt.ylabel("RPS", fontsize=18)
plt.axis(ymin=0, xmin=0, xmax=tenminuteseconds[-1])
plt.yticks(fontsize=18)
plt.xticks(fontsize=18)
plt.grid()
plt.title("EVALUATION TRAFFIC TRACE", fontsize=18)
plt.show()


first10Minute = listCount[0:600000]
tenminute = setAllTimestamp[0:600000]




#plt.plot(tenminute, first10Minute)
#plt.xlabel("Time [ms]")
#plt.ylabel("Number of requests")
#plt.title("Number of requests over 10 minutes")
#plt.show()

new = np.add.reduceat(first10Minute, np.arange(0, len(first10Minute), 1000))


tenminuteseconds = list(range(0,600))
#plt.plot(tenminuteseconds, new)
#plt.xlabel("TIME [s]", fontsize=18)
#plt.xticks(fontsize=18)
#plt.yticks(fontsize=18)
#plt.ylabel("REQUESTS",fontsize=18)
#plt.axis(ymin=0, xmin=0, xmax=599)
#plt.grid()
#plt.title("NUMBER OF REQUESTS OVER 10 MINUTES",fontsize=18)
#plt.show()

first3Minute = listCount[0:180000]
threeminute = setAllTimestamp[0:180000]


new = np.add.reduceat(first3Minute, np.arange(0, len(first3Minute), 1000))


threeminuteseconds = list(range(0,180))


first10Minute = listCount[600000:1200000]


new2 = np.add.reduceat(first10Minute, np.arange(0, len(first10Minute), 1000))


tenminuteseconds = list(range(0,600))
plt.plot(tenminuteseconds, new2)
plt.xlabel("TIME [s]", fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel("RPS",fontsize=18)
plt.axis(ymin=0, xmin=0, xmax=599)
plt.grid()
plt.title("HPA ANALYSIS TRAFFIC TRACE",fontsize=18)
plt.show()

first3Minute = listCount[0:180000]
threeminute = setAllTimestamp[0:180000]



last3Minute = listCount[420000:600000]
threeminute = setAllTimestamp[0:180000]


new2 = np.add.reduceat(last3Minute, np.arange(0, len(last3Minute), 1000))


threeminuteseconds = list(range(0,180))

zeros = np.zeros(120)
total = np.concatenate((new,zeros, new2), axis=None)
sixminuteseconds = list(range(0,480))
plt.plot(sixminuteseconds, total)
plt.xlabel("TIME [s]", fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel("RPS",fontsize=18)
plt.axis(ymin=0, xmin=0, xmax=sixminuteseconds[-1])
plt.grid()
plt.title("TRAINING TRAFFIC TRACE",fontsize=18)
plt.show()












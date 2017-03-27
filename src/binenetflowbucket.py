'''
Code for bucketing argus netflows into time windows.
'''

import pandas as pd
import numpy as np

#Function to convert absolute time into seconds 
def unixTimetoSeconds(a):
    return a.value/1000000000
'''
The function splits flows which spread across multiple time windows into multiple buckets 
and take average of their features like total destination bytes. total packets etc.
'''
def bucket(df, timeWindow = 60):
	df['unixstarttime']=pd.to_datetime(df.StartTime, format='%Y-%m-%dT%H:%M:%S').apply(unixTimetoSeconds)
	#making starttime and stoptime absolute
	ref=min(df.unixstarttime)
	df.unixstarttime=df.unixstarttime-ref
	#sorting data according to ['unixstarttime' 'unixstoptime']
	df.sort_values(by='unixstarttime',inplace=True)
	tot=len(df)
	ndf=pd.DataFrame(columns=list(df.columns))
	ndf['bucket']=[]
	x=0
	
	for index, raw in df.iterrows():
	    x=x+1
	    if x%10 == 0:
	        print "----------"+str(x*100.0/tot)+"-----------"
	        start = raw.unixstarttime/timeWindow
	        diff=int(raw.Dur/timewWindow)
	        for i in range(diff):
	            temp=[raw.StartTime,raw.Dur,raw.Proto,raw.SrcAddr,raw.Sport,raw.Dir,raw.DstAddr,raw.Dport,raw.State,raw.sTos*1.0/diff,raw.dTos*1.0/diff,raw.TotPkts*1.0/diff,raw.TotBytes*1.0/diff,raw.SrcBytes*1.0/diff,raw.Label,raw.unixstarttime,start+i]
	            ndf.loc[len(ndf)]=temp
	return ndf

df = pd.read_csv("/home/ankit/Desktop/MTP/Database/CTU/capture20110810.binetflow")
ndf = bucket(df)

ndf.to_csv("/home/ankit/Desktop/MTP/Database/CTU/capture20110810.binetflow.ndf")



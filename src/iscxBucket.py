'''
The code buckets netflows of ISCX Dataset in one minute time windows.
'''

import glob
import pandas as pd
import numpy as np
import os.path

#Conver unix time to seconds
def unixTimetoSeconds(a):
    return a.value/1000000000

def bucket(filename, timeWindow = 60):
	if os.path.exists('/home/alok/Documents/Dataset/Current_training_ICSX_dataset/ndf/'+filename[64:-4]+'_ndf.csv'):
		print filename[64:-4]+"_ndf.csv already exists! Skipping..."
		return
	print "Staring "+filename[64:]
	df=pd.read_csv(filename)
	df['unixstarttime']=pd.to_datetime(df.startDateTime, format='%Y-%m-%dT%H:%M:%S').apply(unixTimetoSeconds)
	df['unixstoptime']=pd.to_datetime(df.stopDateTime, format='%Y-%m-%dT%H:%M:%S').apply(unixTimetoSeconds)

	#making starttime and stoptime absolute
	ref=min(df.unixstarttime)
	df.unixstarttime=df.unixstarttime-ref
	df.unixstoptime=df.unixstoptime-ref

	#sorting data according to ['unixstarttime' 'unixstoptime']
	df.sort('unixstarttime',inplace=True)
	tot=len(df)
	ndf=pd.DataFrame(columns=list(df.columns))
	ndf['bucket']=[]
	ndf=ndf.drop(['Unnamed: 0'],axis=1)
	x=0
	for index, raw in df.iterrows():
		x=x+1
		if x%10 == 0:
			print "----------"+str(x*100.0/tot)+"-----------"
		start=raw.unixstarttime/timeWindow
		stop=raw.unixstoptime/timeWindow
		diff=stop-start+1
		for i in range(diff):
			#print str(i)+"/"+str(diff)
			temp=[raw.appName,int(raw.totalSourceBytes)/diff,int(raw.totalDestinationBytes)/diff,int(raw.totalDestinationPackets)/diff,int(raw.totalSourcePackets)/diff,raw.sourcePayloadAsBase64,raw.sourcePayloadAsUTF,raw.direction,raw.sourceTCPFlagsDescription,raw.destinationTCPFlagsDescription,raw.source,raw.protocolName,raw.sourcePort,raw.destination,raw.startDateTime,raw.stopDateTime,raw.Tag,raw.destinationPayloadAsBase64,raw.destinationPayloadAsUTF,raw.destinationPort,raw.unixstarttime,raw.unixstoptime,start+i]
			ndf.loc[len(ndf)]=temp
	ndf.to_csv('/home/alok/Documents/Dataset/Current_training_ICSX_dataset/ndf/'+filename[64:-4]+'_ndf.csv')
	print filename[64:-4]+'_ndf.csv done!'

filename=glob.glob("/home/alok/Documents/Dataset/Current_training_ICSX_dataset/flow/*")
#print filename
for f in filename:
	bucket(f)

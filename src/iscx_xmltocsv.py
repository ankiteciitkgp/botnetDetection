'''
This code converts XML files of ISCX ataset to CSV files with all the features present in the file
'''

import pandas as pd
from lxml import etree

appName=[]
totalSourceBytes=[]
totalDestinationBytes=[]
totalDestinationPackets=[]
sensorInterfaceId=[]
totalSourcePackets=[]
sourcePayloadAsBase64=[]
sourcePayloadAsUTF=[]
destinationPayloadAsBase64=[]
destinationPayloadAsUTF=[]
direction=[]
sourceTCPFlagsDescription=[]
destinationTCPFlagsDescription=[]
source=[]
protocolName=[]
sourcePort=[]
destination=[]
destinationPort=[]
startDateTime=[]
stopDateTime=[]
Tag=[]
df=pd.DataFrame()

xmlfile=etree.parse('/home/alok/Documents/Dataset/Current_training_ICSX_dataset/TestbedThuJun17-1Flows.xml')
root=xmlfile.getroot()
df=pd.DataFrame()
for e in root.getiterator():
    if e.tag=='appName':
        appName.append(e.text)
    elif e.tag=='totalSourceBytes':
        totalSourceBytes.append(e.text)
    elif e.tag=='totalDestinationBytes':
        totalDestinationBytes.append(e.text)
    elif e.tag=='totalDestinationPackets':
        totalDestinationPackets.append(e.text)
    elif e.tag=='sensorInterfaceId':
        sensorInterfaceId.append(e.text)
    elif e.tag=='totalSourcePackets':
        totalSourcePackets.append(e.text)
    elif e.tag=='sourcePayloadAsBase64':
        sourcePayloadAsBase64.append(e.text)
    elif e.tag=='sourcePayloadAsUTF':
        sourcePayloadAsUTF.append(e.text)
    elif e.tag=='direction':
        direction.append(e.text)
    elif e.tag=='sourceTCPFlagsDescription':
        sourceTCPFlagsDescription.append(e.text)
    elif e.tag=='destinationTCPFlagsDescription':
        destinationTCPFlagsDescription.append(e.text)
    elif e.tag=='source':
        source.append(e.text)
    elif e.tag=='protocolName':
        protocolName.append(e.text)
    elif e.tag=='sourcePort':
        sourcePort.append(e.text)
    elif e.tag=='destination':
        destination.append(e.text)
    elif e.tag=='startDateTime':
        startDateTime.append(e.text)
    elif e.tag=='stopDateTime':
        stopDateTime.append(e.text)
    elif e.tag=='Tag':
        Tag.append(e.text)
    elif e.tag=='destinationPayloadAsBase64':
        destinationPayloadAsBase64.append(e.text)
    elif e.tag=='destinationPayloadAsUTF':
        destinationPayloadAsUTF.append(e.text)
    elif e.tag=='destinationPort':
        destinationPort.append(e.text)
    else :
        pass


df['appName']=appName
df['totalSourceBytes']=totalSourceBytes
df['totalDestinationBytes']=totalDestinationBytes
df['totalDestinationPackets']=totalDestinationPackets
#df['sensorInterfaceId']=sensorInterfaceId
df['totalSourcePackets']=totalSourcePackets
df['sourcePayloadAsBase64']=sourcePayloadAsBase64
df['sourcePayloadAsUTF']=sourcePayloadAsUTF
df['direction']=direction
df['sourceTCPFlagsDescription']=sourceTCPFlagsDescription
df['destinationTCPFlagsDescription']=destinationTCPFlagsDescription
df['source']=source
df['protocolName']=protocolName
df['sourcePort']=sourcePort
df['destination']=destination
df['startDateTime']=startDateTime
df['stopDateTime']=stopDateTime
df['Tag']=Tag
df['destinationPayloadAsBase64']=destinationPayloadAsBase64
df['destinationPayloadAsUTF']=destinationPayloadAsUTF
df['destinationPort']=destinationPort

df.to_csv('/home/alok/Documents/InfoSec/MTP_code/files/flow/17junflow1.csv')

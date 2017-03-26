def getBuckets(df):
    df=df.drop(0)
    #df=df.drop(65692) # max Dur is eliminated
    def getvalue(a):
        return a.value/1000000000
    startTime=pd.to_datetime(df.StartTime, format='%Y/%m/%d %H:%M:%S').apply(getvalue)
    ref=min(startTime)
    startTime=startTime-ref
    ndf=pd.DataFrame(columns=list(df.columns))
    ndf['bucket']=[]
    for index, row in df.iterrows():
        diff=int(row.Dur/60)+1
        print index
        for i in range(diff):
            temp=[row.StartTime,row.Dur,row.Proto,row.SrcAddr,row.Sport,row.Dir,row.DstAddr,row.Dport,row.State,row.sTos,row.dTos,row.TotPkts/diff,row.TotBytes,startTime+i]
            ndf.loc[len(ndf)]=temp
    return ndf






# function to get ISCX dataset for testing 
def getISCXFeatures(df):
    df.Sport=df.Sport.apply(str)
    df.bucket=df.bucket.apply(str)
    df.SrcAddr=df.SrcAddr.apply(str)
    df.DstAddr=df.DstAddr.apply(str)
    df.Dport=df.Dport.apply(str)
    group = df.groupby(["bucket","SrcAddr"])
    features = group.Sport.nunique()
    features = pd.DataFrame(features)
    features.rename(columns={'Sport':'usrc_port'},inplace=True)
    features['udest_ip'] = group.DstAddr.nunique()
    features['udest_port'] = group.Dport.nunique()
    features['netflows'] = group.DstAddr.count()
    features['bytes'] = group.TotBytes.sum()
    features['packets'] = group.TotPkts.sum()
    #I dont know what this next line does
    #getFeatures had it :p
    features.reset_index(inplace=True)
    return features

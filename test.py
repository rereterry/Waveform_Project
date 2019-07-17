import time  
import sys
import json  
import random
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from pandas.core.frame import DataFrame
import importlib
import matplotlib.pyplot as plt
import itertools


# In[2]:


def trim4CSV(str):
    str1 = str.replace('"','')
    str2 = str1.replace('[','')
    str3 = str2.replace(']','')
    str4 = str3.replace('{','')
    str5 = str4.replace('}','')
    str6 = str5.replace('(','')
    str7 = str6.replace(')','')
    str8 = str7.replace('\n','')
    str9 = str8.replace(',','，')
    return str9



# In[3]:

from keras.models import load_model    
import matplotlib.pyplot as plt
import codecs
import paho.mqtt.client as mqtt
import scipy.stats as stats
from scipy.signal import correlate


# In[4]:


def Average(lst): 
    return sum(lst) / len(lst) 


# In[5]:


#Cut some thing we don't want
def first_cut(one_flow, end):
    count1 = end-2
    while True:
        count1 -= 1
        if(Average(one_flow[count1-2:count1+2])> one_flow[end+1]) :
            break
    return count1


# In[6]:


#cut some thing we don't want
def end_cut(one_flow, start, end):
    count2 = end
    
    while (one_flow[count2] > one_flow[start]):
        count2 -= 1
        
        if (Average(one_flow[count2-2:count2+2]) > one_flow[start] ) and (one_flow[count2]<=1.5 and one_flow[count2] >= 1) :
            break

    
    while (one_flow[count2] <= 1) :
        count2 -= 1
    
    
    return count2


# In[7]:



# In[8]:

from keras import backend as K
from IPython.display import clear_output
import csv

def data_predict(result,model,distarry,tstart):
    result.to_csv('storagecache.csv', encoding='utf_8_sig', index=False, header=None)
    resultt = pd.read_csv('storagecache.csv',sep=',', header=None)
    testvec=resultt.iloc[0]


    series=np.array(testvec)[8:]
    series2=np.array(testvec)[1:8]
    
    #Array length
    d_length =np.array(testvec)[5]
    
    #type of component
    partno =np.array(testvec)[1]
    partno = partno.replace('-','')
    partno = partno[5:7]
    print(partno)
    
    NowTime = np.array(testvec)[7]
    NowTime = NowTime.replace('-','')
    NowTime = NowTime[0:3]

    
    deviceid = np.array(testvec)[6]
    print('Now we begin to predict')
    global count
    
    if(d_length <= 100):
        print('電流比數少於100筆，非正常現象')
        resultt.to_csv('Wrong_length_'+fn+'.csv', encoding='utf_8_sig', mode='a', index=False, header=None)
    model1 = model
    distarr = distarry
    mechine = fn[0:4]
    component = fn[5:]
    if(deviceid == mechine):
        if(partno == component): 

            n_samples, dim, sigma = 1000, 3, 4
            n_bkps = 4  # number of breakpoints
            dataseries = series
            length1 = first_cut(series, 40)
            print('start point ', length1)
            
            length2 = end_cut(dataseries, length1, len(dataseries)-40)
            print('end point ', length2)
            new_length = length2-length1
            print("New current length ", new_length)
            
        

            if(new_length/len(series) > 0.8):
                print("Now we check the pic")
                tstart = time.time()
                post_contents = []    
#                 rpt.display(np.array(dataseries), bkps, point_result, figsize=(10, 2))
#                 plt.show()


                start = length1
                end = length2
                data2_len = end - start
                print('Cut value ' , dataseries[end])
                dataseries2 = dataseries[start:end]
                test2=np.zeros((1,4))
                idx=int(series2[3])
                print('idx ok')
                disuse = distarr[idx-1]
                len1 = len(dataseries2)
                len2 = len(disuse)
                print('dataseries2 length ',len1,'Model length ', len2)

                if(data2_len <= len2):
                    
                    corr = correlate(disuse, dataseries2)
                    lag = np.argmax(corr)
                    print('lag ', lag)
                    if(lag < len1 and lag < len2) :
                        new_disuse = disuse[0:lag]
                        new_ds = dataseries2[len1-lag : len1]
                    else :
                        new_disuse = disuse[lag-len1:lag]
                        new_ds = dataseries2
                        
                    Correlation = stats.pearsonr(new_disuse, new_ds)[0]                    
                    print('Correlation ', Correlation)
                    try: 
                        print('yes, inside the try')
                        test2[0][0]=np.sqrt(np.sum((new_ds - new_disuse) ** 2))
                    except Exception as e:                    
                        print('test2 ERROR ', e)
                    else : 
                        print('test2 success ')
                    tt=np.array(test2)
                    predicted_test = model1.predict(tt)
                    MSE = []
                    n = tt.shape[1]
                    for i in range(len(tt)):
                        MSE.append( np.sum((tt[i] - predicted_test[i])**2)/n)
                    MSE = np.array(MSE)
                else :
                    

                    corr = correlate(dataseries2, disuse)
                    lag = np.argmax(corr)
                    print('lag ', lag)
                    if(lag < len1 and lag < len2):
                        new_ds = dataseries2[0:lag]
                        new_disuse = disuse[len2-lag : len2]
                    else:
                        new_ds = dataseries2[lag-len2:lag]
                        new_disuse = disuse
                    
                    Correlation = stats.pearsonr(new_disuse, new_ds)[0] 
                    print('Correlation ', Correlation)
                    

                    try: 
                        print('yes, inside the try')
                        test2[0][0]=np.sqrt(np.sum((new_ds - new_disuse) ** 2))
                    except Exception as e:                    
                        print('test2 ERROR ', e)
                    else : 
                        print('test2 success ')
                    tt=np.array(test2)
                    predicted_test = model1.predict(tt)
                    MSE = []
                    n = tt.shape[1]
                    for i in range(len(tt)):
                        MSE.append( np.sum((tt[i] - predicted_test[i])**2)/n)
                    MSE = np.array(MSE)
                
                print('MSE ', MSE)
                if(MSE > 1) :  
                    resultt.to_csv('abnormal_'+fn+'.csv', encoding='utf_8_sig', mode='a', index=False, header=None)
                    timestamp = NowTime

                    #序號      
                    Serial_num.append(partno)
                    if len(Serial_num)<10:
                        SN = '00' + str(len(Serial_num))
                    if len(Serial_num)>=10 and len(Serial_num)<100:
                        SN = '0' + str(len(Serial_num))
                    if len(Serial_num)>=100:
                        SN = str(len(Serial_num))

                    payload = timestamp + SN
                   
                    client.publish('Mitac/ErrorMsg/errorTry',payload,0, False)

                    print('Abnormal component Waveform')
                else:
                    print('normal')
                tEnd = time.time()
                GP_time = tEnd-tstart
                print("get and post using time : ",GP_time)
                tEnd =0
                K.clear_session()
                print('Clean model')
                count += 1
                print("Check whether we get the count number ", count)
                if count == 300 :
                    count -= 300
                    clear_output()
                print('-------------------------------------------------------------------------------------')
               
            else:
                print('Out of 80%')
                resultt.to_csv('Less_len_'+fn+'.csv', encoding='utf_8_sig', mode='a', index=False, header=None)
                print('-------------------------------------------------------------------------------------')

        else:
            print('not W4')


    else :
        print('Not '+fn)


# ### 欄位設定

# In[9]:


import paho.mqtt.client as mqtt
# from keras.models import load_model


#設定欄位
subject = ['設備模式', 'partno', '電流監控取樣', '絲攻壽命_SV', '絲攻壽命_PV', '電流監控筆數', 'DeviceID', 'Nowtime']
textdata = [('1', '2', '3', '4', '5', '6', '7', '8')]
df = pd.DataFrame(textdata,columns = subject)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
#     client.subscribe("IOT_NEAT_TOPIC01")


def on_message(client, userdata, msg):
    
    global fn 
    print('ok, we get the msg')
    fn = msg.topic[11:]
    modelname = 'fonda_model_crest_'+fn+'.h5'
    try :       
        model1 = load_model(modelname)
    except Exception as e:
        print(e)   
    print('model ok')
    distarr=np.loadtxt('dist_'+fn+'.txt', delimiter=",")
    print('ok_crest')
    tstart = time.time()
    tp22txt = str(msg.payload.decode(encoding="utf-8"))
    fp = open(fn+'_log.txt', "a")
    fp.write(tp22txt)
    fp.write('\n')
    fp.close()       
    
   
    tstart = time.time()
    
    
    
    payload_dict =str(msg.payload.decode(encoding="utf-8"))
    data = json.loads(payload_dict)
    
    devicemode = data.get('設備模式')
#     print(devicemode)
    df.iat[0,0] = devicemode
    
    datarange = data.get('電流監控筆數')
#     print(datarange)
    df.iat[0,5] = datarange
    
    NowTime = data.get('NowTime')
#     print(NowTime)
    df.iat[0,7] = NowTime
    
    deviceid = data.get('DeviceID')
#     print(deviceid)
    df.iat[0,6] = deviceid
    
    cycletime = data.get('電流監控取樣頻率時間_ms')
#     print(cycletime)
    df.iat[0,2] = cycletime
    
    countmaxvalue = data.get('絲攻壽命_SV')
#     print(countmaxvalue)
    df.iat[0,3] = countmaxvalue
    
    counter = data.get('絲攻壽命_PV')
#     print(counter)
    df.iat[0,4] = counter
    
    partno = data.get('PartNo')
#     print(partno)
    df.iat[0,1] = partno
    
    currentmatrix = data.get('電流矩陣')
#     print(currentmatrix)
    
    data_contents = []
    current_matrix = trim4CSV(str(currentmatrix))
    data_array = current_matrix.split('，')
    data_contents.append(data_array)
#     print(data_contents)
    df2 = pd.DataFrame(data_contents)
    
    
    if(df.iat[0,0] == '自動'):
        result = pd.concat([df, df2], axis=1)
        data_predict(result,model1,distarr, tstart)
            
            


# ### 接收值

# In[10]:


# while True:
Serial_num = []
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883)
count = 0
fn = 'tp'
client.subscribe('mechine1/con2/+',qos=0)
client.subscribe('Nafco/feedbackToEdge',qos=0)
client.loop_forever()
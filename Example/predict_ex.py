import os
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
from IPython.display import clear_output
import scipy.stats as stats
from scipy.signal import correlate
import paho.mqtt.client as mqtt


### 讀取資料
def read_test(TP, model_keras) :   
    try:
        with open('./log/Pre_' + TP + '.txt', "r") as f:
            payload = f.read()
            f.close()
            if payload in set_test :
                print('It has been predict')
            else :
                set_test.add(payload)
                #正式開始預測
                info_josn(payload, TP, model_keras)
            
    except IOError:
        print('No input file')

def info_josn(payload, fn, model_keras) :
    # Here use to design your payload
    df = pd.DataFrame(textdata,columns = subject)
    data = json.loads(payload)
    model_name = 'model_' + deviceid + '_' + partno + '.h5'        
    model_tp_partno = model_keras[model_name]
    if(df.iat[0,0] == 'Auto'):
        result = pd.concat([df, df2], axis=1)
        try :       
            data_predict(result, model_tp_partno, tstart, fn)
            
        except Exception as ep:
            print(ep)

def mqtt_publish(topic, payload) :
    client = mqtt.Client()
    client.connect('10.32.3.200', 1883)
    client.publish(topic , payload, 0, False)
    client.loop_start()

def error_part(NowTime, partno, fn, resultt, deviceid) :
    
    try :
        resultt.to_csv('./abnormal/abnormal_' + deviceid + '_' + partno.replace('-','') + '_' + NowTime + '.csv', encoding='utf_8_sig', mode='a',
                    index=False, header=None)
    except Exception :
        print('Save error fail')
    
    payload = '............'
    output_str = deviceid + partno.replace('-','') + '-' + str(payload) + '-' + flow 
    ouput_topic = 'MQTT/feedback/Ans/' + fn
    mqtt_publish(ouput_topic , output_str)


def data_predict(result, model, tstart, fn):
    #     tstart = 0
        result.to_csv('storagecache.csv', encoding='utf_8_sig', index=False, header=None)
        resultt = pd.read_csv('storagecache.csv',sep=',', header=None)
        testvec=resultt.iloc[0]
        series2=np.array(testvec)[1:8]
        NowTime = np.array(testvec)[7]
        Ans = model.predict(series2)
        if Ans is 1 :
            print('Normal')
        else :
            error_part(NowTime, partno, fn, resultt, deviceid)

def clean_pre_txt() :
    all_pre_in_directory = os.listdir('./log')
    if len(all_pre_in_directory) == 0 :
        print('no file')
    else :
        for tmp in all_pre_in_directory: 
            file_path = './log/' + tmp
            if tmp.find('.txt') != -1 and tmp[:3] == 'Pre':
                os.remove(file_path)

def pre_main() :
    #clean old txt
    clean_pre_txt()
    #read all model
    model_keras = all_model('./model')
    while True :
        read_test('test1', model_keras)
        read_test('test2', model_keras)
        time.sleep(2)

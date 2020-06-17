import time
import sys
import json
import random
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from pandas.core.frame import DataFrame
import itertools
import codecs
import csv
import paho.mqtt.client as mqtt
import os


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    
    print('Ok, we get the msg')
    len_name = len(msg.topic)
    fn = msg.topic[len_name - 5:len_name]
    
    if fn == 'test1' or fn == 'test2' :
        payload_dict =str(msg.payload.decode(encoding="utf-8"))
        data = json.loads(payload_dict)
    
        devicemode = data.get('Devicemode')
        deviceid = data.get('DeviceID')
        partno = data.get('PartNo')

        if len(partno) > 3 :
            print('有料號')
            
            tp_txt = payload_dict
            log_name = './log/Log_' + deviceid + '_' + partno + '.txt'
            fp = open(log_name, "a")
            fp.write(tp_txt)
            fp.write('\n')
            fp.close()
            
            if devicemode == 'Auto' :
                
                log_name = './log/Pre_' + deviceid + '.txt'
                fp = open(log_name, "w")
                fp.write(tp_txt)
                fp.write('\n')
                fp.close()
                # predict read txt to save in set
            else :
                print('Not Auto')
        
        else :
            print('No part number')
        
    else :
        print('Not test1/test2')

def mqtt_main() :
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    IP = "xx.xx.xx.xxx"
    client.connect(IP, 1883)
    client.subscribe('MQTT/Edge/+', qos=0)
    # client.subscribe('nafco_json',qos=0)
    client.subscribe('Nafco/feedbackToEdge', qos=0)
    # client.loop_start()
    client.loop_forever()

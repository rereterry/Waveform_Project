# Waveform_Project
This project is a simple example to use node-red, mqtt, to present Remote transmission of messageswant and predict whether the new waveform is match normal situation. 
Mutilpe model and Mutilpe input waveform can use
# Environment
Python 3.6.1
Python Library
tensorboard          1.14.0   
tensorflow           1.14.0   
tensorflow-estimator 1.14.0   
tensorflow-gpu       1.1.0  
requests             2.22.0   
paho-mqtt            1.4.0    
Keras                2.2.4    
Keras-Applications   1.0.8    
Keras-Preprocessing  1.1.0   
# Node Red Structure
[{"id":"b799e0f6.a49c2","type":"inject","z":"ee8fdf5a.b11b8","name":"","topic":"","payload":"","payloadType":"date","repeat":"","crontab":"","once":false,"onceDelay":0.1,"x":120,"y":100,"wires":[["b6f280b2.24986"]]},{"id":"b6f280b2.24986","type":"file in","z":"ee8fdf5a.b11b8","name":"test file","filename":"","format":"lines","chunk":false,"sendError":false,"encoding":"none","x":300,"y":100,"wires":[["ae1a195f.34d8e8"]]},{"id":"ae1a195f.34d8e8","type":"delay","z":"ee8fdf5a.b11b8","name":"","pauseType":"rate","timeout":"3","timeoutUnits":"seconds","rate":"1","nbRateUnits":"4","rateUnits":"second","randomFirst":"1","randomLast":"5","randomUnits":"seconds","drop":false,"x":500,"y":100,"wires":[["31230654.6604ba"]]},{"id":"31230654.6604ba","type":"mqtt out","z":"ee8fdf5a.b11b8","name":"","topic":"MQTT/Edge/test","qos":"","retain":"","broker":"fb39f3b3.efc94","x":730,"y":100,"wires":[]},{"id":"1c4e7c69.cd8ab4","type":"mqtt in","z":"ee8fdf5a.b11b8","name":"","topic":"MQTT/Edge/test","qos":"2","datatype":"auto","broker":"fb39f3b3.efc94","x":120,"y":200,"wires":[["85c8854e.4befd8"]]},{"id":"85c8854e.4befd8","type":"debug","z":"ee8fdf5a.b11b8","name":"","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"false","x":310,"y":200,"wires":[]},{"id":"4fe115b1.ff624c","type":"mqtt in","z":"ee8fdf5a.b11b8","name":"","topic":"MQTT/feedback/Ans","qos":"2","datatype":"auto","broker":"fb39f3b3.efc94","x":130,"y":300,"wires":[["c6f0bca1.278f8"]]},{"id":"c6f0bca1.278f8","type":"debug","z":"ee8fdf5a.b11b8","name":"","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"false","x":340,"y":300,"wires":[]},{"id":"fb39f3b3.efc94","type":"mqtt-broker","z":"","name":"","broker":"","port":"1883","clientid":"","usetls":false,"compatmode":true,"keepalive":"60","cleansession":true,"birthTopic":"","birthQos":"0","birthPayload":"","closeTopic":"","closeQos":"0","closePayload":"","willTopic":"","willQos":"0","willPayload":""}]

# Operation process
Use matt, node-red to transmit signals, let python receive, and then use the obtained msg topic as the basis for selecting which model. Finally, you can use the topic to distinguish the stored files. If there is an error, then use the publish method to output which Pen data error

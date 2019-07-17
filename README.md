# Waveform_Project
This project want to predict whether the new waveform is match normal situation.   
Use node-red, mqtt, to present Remote transmission of messages  
Mutilpe model and Mutilpe input waveform
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
[{"id":"ee8fdf5a.b11b8","type":"tab","label":"test_load_file","disabled":false,"info":""},{"id":"16562d15.a0b093","type":"inject","z":"ee8fdf5a.b11b8","name":"","topic":"","payload":"","payloadType":"date","repeat":"","crontab":"","once":false,"onceDelay":0.1,"x":120,"y":100,"wires":[["6cf23c87.466fb4"]]},{"id":"6cf23c87.466fb4","type":"pythonshell in","z":"ee8fdf5a.b11b8","name":"","pyfile":"/Users/{user name}/Desktop/test.py","virtualenv":"","continuous":false,"stdInData":false,"x":400,"y":100,"wires":[["abf6849d.6ecf58"]]},{"id":"abf6849d.6ecf58","type":"debug","z":"ee8fdf5a.b11b8","name":"","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"false","x":650,"y":100,"wires":[]},{"id":"ae28ed3b.1adcd","type":"mqtt out","z":"ee8fdf5a.b11b8","name":"","topic":"mechine1/con1","qos":"","retain":"","broker":"e30ae943.83f5e8","x":660,"y":240,"wires":[]},{"id":"f2ca4ab5.5a9e58","type":"mqtt out","z":"ee8fdf5a.b11b8","name":"","topic":"mechine2/con2","qos":"","retain":"","broker":"e30ae943.83f5e8","x":660,"y":300,"wires":[]},{"id":"9506ee7d.0ca9f","type":"mqtt out","z":"ee8fdf5a.b11b8","name":"","topic":"mechine3/con1","qos":"","retain":"","broker":"e30ae943.83f5e8","x":660,"y":360,"wires":[]},{"id":"a2f56ad4.b10368","type":"inject","z":"ee8fdf5a.b11b8","name":"","topic":"","payload":"","payloadType":"json","repeat":"","crontab":"","once":false,"onceDelay":0.1,"x":390,"y":240,"wires":[["ae28ed3b.1adcd"]]},{"id":"c1192c04.b107d","type":"mqtt in","z":"ee8fdf5a.b11b8","name":"","topic":"mechine/wrong","qos":"2","datatype":"auto","broker":"6843f326.7e892c","x":660,"y":480,"wires":[["13b6c881.8ec197"]]},{"id":"13b6c881.8ec197","type":"debug","z":"ee8fdf5a.b11b8","name":"","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"false","x":930,"y":480,"wires":[]},{"id":"e30ae943.83f5e8","type":"mqtt-broker","z":"","name":"master","broker":"127.0.0.1","port":"1883","clientid":"","usetls":false,"compatmode":true,"keepalive":"60","cleansession":true,"birthTopic":"","birthQos":"0","birthPayload":"","closeTopic":"","closeQos":"0","closePayload":"","willTopic":"","willQos":"0","willPayload":""},{"id":"6843f326.7e892c","type":"mqtt-broker","z":"","name":"","broker":"10.32.2.14","port":"1883","clientid":"","usetls":false,"compatmode":true,"keepalive":"60","cleansession":true,"birthTopic":"","birthQos":"0","birthPayload":"","closeTopic":"","closeQos":"0","closePayload":"","willTopic":"","willQos":"0","willPayload":""}]

# Operation process
Use matt, node-red to transmit signals, let python receive, and then use the obtained msg topic as the basis for selecting which model. Finally, you can use the topic to distinguish the stored files. If there is an error, then use the publish method to output which Pen data error

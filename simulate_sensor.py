import time
import paho.mqtt.client as mqtt
import json
import ssl
import random

broker = "<broker_url here>"
port = 8883
topic = "iot-2/evt/test/fmt/json"
username = "<username here>"
password = "<password_here>"  
organization = "<org id here>"                   
deviceType = "Python_Client"

mqttc = mqtt.Client("<client id here>")
print(username+' '+password)
mqttc.username_pw_set(username,password)
mqttc.tls_set_context(context=None)
mqttc.tls_insecure_set(False)
mqttc.connect(broker,8883,60)

for i in range(0,10):
        #print("msg : ",msg)
        #msg={'reading'+str(i):{'temperature': i}}
        print('Sending sample gravity sensor values')
        msg={'time':i,'gravity_x':random.randrange(1,50)}
        mqttc.publish(topic,json.dumps(msg))
        #time.sleep(1)

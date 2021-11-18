# Subscribes to Data Published to AWS Cloud

import paho.mqtt.client as mqtt
import os
import socket
import ssl
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

#Ahora definimos el pin 11
GPIO.setup(12, GPIO.OUT) 





def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#" , 1 )

def on_message(client, userdata, msg):

    
    print("topic: "+msg.topic)
    print(str(msg.payload))
    if msg.topic == "LEDON":
        
       print("PRENDE")
       
       GPIO.output(12, GPIO.LOW)
        
    if msg.topic == "LEDOFF": 
       print("APAGA")
       GPIO.output(12, GPIO.HIGH)
           






mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message


# Define the AWS Host Key  ; Thing Name defined in AWS IoT; Root Certificate Path; Certificate Path; Private Key Certificate Path  
awshost = "a2ednx02go12nb-ats.iot.us-east-2.amazonaws.com"
# AWS Port(Default: 8883)
awsport = 8883
# Client ID
clientId = "raspi"
# Thing Name defined in AWS IoT
thingName = "raspi"
# Root Certificate Path
caPath = "AmazonRootCA1.pem"
# Certificate Path
certPath = "5e3fb7bd94-certificate.pem.crt"
# Private Key Certificate Path
keyPath = "5e3fb7bd94cf6f3d2580f5424df747139677d88405ddceb48e8f52a273d367ed-private.pem.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqttc.connect(awshost, awsport, keepalive=60)
mqttc.loop_forever()

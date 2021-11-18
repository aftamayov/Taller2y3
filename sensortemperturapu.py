import time                             
import csv
import requests
from w1thermsensor import W1ThermSensor #Importamos el paquete W1ThermSensor
import adafruit_adxl34x

start_time  =  time.time()


sensor = W1ThermSensor() 
contador = 0;
promedio = 0;
promedio2 = 0;
while True:
    contador = contador +1
    temperature = sensor.get_temperature()                #Obtenemos la temperatura en centígrados
    print(temperature)
    promedio = promedio + temperature
    elapsed_time = time.time() - start_time
    if elapsed_time >=60:
        print("Envia a cloud")
        promedio2=promedio/contador
        enviar= requests.get("https://api.thingspeak.com/update?api_key=7VWSMAZ5QUIYXGAZ&field1="+str(promedio2))
        start_time  =  time.time()
    else:
        time.sleep(1)                                        #Esperamos un segundo antes de terminar el ciclo

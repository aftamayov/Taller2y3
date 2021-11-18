import time
import serial
import queue
import threading
import statistics
import pt2_i2c as I2C
import subprocess

ser = None
RxTx = queue.Queue()
xI2CTx = queue.LifoQueue() 
yI2CTx = queue.LifoQueue()
zI2CTx = queue.LifoQueue()

def TempThread():
    """
    Función que ejecuta el codigo bash para capturar datos del sensor de temperatura 
    """
    while 1:
        subprocess.call("./tempbash.sh")
        time.sleep(1)
        
def I2CThread():
    """
    Función que captura los datos del sensor I2C
    """
    while 1:
        I2C.i2cRTX()
        xI2CTx.put(I2C.xAccl)
        yI2CTx.put(I2C.yAccl)
        zI2CTx.put(I2C.zAccl)


def RxThread():
    """ 
    Función que recibe datos del serial, verifica si el mensaje enviado es valido o no.
    """
    while 1:
       x = '#'
       if ser.inWaiting() > 0:
        while ser.inWaiting() > 0:
           
            aux = ser.read()
            x = x + aux
        RxTx.put(x)
        print(x)
       else:
            time.sleep(0.2)
        
def TxThread():
    """
    Función de calculo de promedio y envio de información por el puerto serial 
    """
    Datos = ['###PROMEDIO','010','##\\n']
    auxN = int(Datos[1])
    
    while 1:
        x = []
        y = []
        z = []
        if RxTx.empty():
            time.sleep(0.2)
        else:
            N = RxTx.get()
            Datos = N.split('-')
        if str(Datos[0]) == '###PROMEDIO' and str(Datos[2]) == ('##' + '\\n'):
            if xI2CTx.empty():
                time.sleep(0.2)
            else:
                if auxN != int(Datos[1]):
                    auxN = int(Datos[1])
                for i in range(auxN):
                    x.append(int(xI2CTx.get()))
                    y.append(int(yI2CTx.get()))
                    z.append(int(zI2CTx.get()))
                PromedioX = statistics.mean(x)
                PromedioY = statistics.mean(y)
                PromedioZ = statistics.mean(z)        
                if ser:
                    Cadena = 'Promedio X =' + str(PromedioX) + 'Promedio Y =' + str(PromedioY) + 'Promedio Z =' + str(PromedioZ)
                    print(Cadena)
                    ser.write(Cadena)
        else:
            print('PROMEDIO INVALIDO')
                    
                
def mainThread(comPortName):
    """
    Función principal 
    """
    global ser 
    ser = serial.Serial \
            (
              port=comPortName,
              baudrate=115200,
              parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              bytesize=serial.EIGHTBITS
            )
    threading.Thread(target=I2CThread).start()
    threading.Thread(target=RxThread).start()
    threading.Thread(target=TxThread).start()
    try:
        while 1:
            time.sleep(1)
    except:
        ser = None
if __name__ == "__main__":
  mainThread("/dev/ttyAMA0")
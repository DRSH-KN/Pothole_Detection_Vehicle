import pynmea2
import serial
import time


def setup_GPS():
    port="/dev/ttyAMA0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    return ser

def get_GPS(gps):
    gps.readline()
    time.sleep(0.001)
    dataout = pynmea2.NMEAStreamReader()
    newdata=gps.readline()
    print(newdata)
    
    if newdata[0:6] == "$GPRMC":
        newmsg=pynmea2.parse(newdata)
        lat=newmsg.latitude
        lng=newmsg.longitude
        gps = str(lat) + "," + str(lng)
        return gps
    else:
        return "0,0"
    
GPS=setup_GPS()
print(get_GPS(GPS))sud
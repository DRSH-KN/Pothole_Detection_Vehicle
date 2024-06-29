import pigpio
import RPi.GPIO as GPIO
import time
import requests
from picamera import PiCamera
import json
from pynmeagps import NMEAReader
import serial

GPIO.setmode(GPIO.BCM)

#indicator Lights
RED = 6
GRN = 5
WHT = 17

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GRN, GPIO.OUT)
GPIO.setup(WHT, GPIO.OUT)

# Initialize ultrasonic sensor
TRIGGER=19
ECHO=13

high_tick = None # global to hold high tick.

DIST=0

def cbfunc(gpio, level, tick):
   global DIST
   global high_tick
   if level == 0: # echo line changed from high to low.
      if high_tick is not None:
         echo = pigpio.tickDiff(high_tick, tick)
         cms = (echo / 1000000.0) * 34030 / 2
         DIST=round(cms, 2)
   else:
      high_tick = tick


# Define GPIO pins for motor control
# These pins correspond to the connections on the L293D motor driver
IN1 = 21  # GPIO pin 20 for controlling one direction of the motor
IN2 = 20
IN3 = 16  # GPIO pin 20 for controlling one direction of the motor
IN4 = 12  # GPIO pin 21 for controlling the other direction of the motor
EN1 = 23  # GPIO pin 27 for controlling the speed of the motor (Enable pin)
EN2 = 24  # GPIO pin 18 for controlling the speed of the motor (Enable pin)

# Set up GPIO pins as output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

PWM_FREQ = 1000

# Function to drive the motor forward
def forward(speed):
    pi.set_PWM_dutycycle(EN1, speed)
    pi.set_PWM_dutycycle(EN2, speed)

    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    

# Function to drive the motor backward
def backward(speed):
    pi.set_PWM_dutycycle(EN1, speed)
    pi.set_PWM_dutycycle(EN2, speed)
    
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    
# Function to stop the motor
def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
# Set the speed to 0

# Set the GPIO pin connected to the servo signal line
SERVO_PIN = 9  # You can use any GPIO pin you prefer
# Set the PWM frequency (Hz)
PWM_FREQ = 50  # Standard frequency for servos

# Function to initialize PWM for the servo
def setup_servo():
    pwm = pigpio.pi()
    pwm.set_mode(SERVO_PIN, pigpio.OUTPUT)
    pwm.set_PWM_frequency(SERVO_PIN, PWM_FREQ)  # Start PWM with 0% duty cycle
    return pwm

def set_servo_angle(pwm, angle):
    # Map the angle to a duty cycle between the min and max limits
    duty_cycle = ((angle / 180.0)*2000 )+501 
    pwm.set_servo_pulsewidth(SERVO_PIN, duty_cycle)
    time.sleep(0.3)  # Wait for the servo to reach th
# Initialize camera
camera = PiCamera()

# Function to capture image
def capture_image(id, name):
    data['id']=id
    with open('/home/pi/Desktop/pothole.json','w') as f:
        json.dump(data, f)
    image_path = "/home/pi/Desktop/images/"+str(id)+name+".jpg"  # Set your desired image path
    time.sleep(2)  # Allow camera to warm up
    camera.capture(image_path)
    return image_path

# Function to send data to server
def send_data_to_server(id,depth,location, image_path1, image_path2):
    url = "https://pottholesitedomain/index.php"
    try:
        with open(image_path1, 'rb') as file1, open(image_path2, 'rb') as file2:
            files = {'image1': file1, 'image2': file2}
            data = {'depth': round(depth,4), 'location': location, 'caseid': id}
            response = requests.post(url, files=files, data=data)
            print("Response:", response.text)
            return response.status_code
    except FileNotFoundError as e:
        print("File not found:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None
    
def setup_GPS():
    port="/dev/ttyAMA0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    return ser

def get_GPS(gps):
    gps.readline()
    time.sleep(0.01)
    
    newdata=gps.readline()
    #print(newdata)
    newdata=newdata.decode()
    #print(newdata)
    newmsg=NMEAReader.parse(newdata)

    #print(newmsg)

    try:
        lat=newmsg.lat
        lng=newmsg.lon
        gps = str(lat) + "," + str(lng)
        return gps
    except:
        return "0,0"

    
def red_indicate():
    GPIO.output(RED, GPIO.HIGH)
    time.sleep(0.4)
    GPIO.output(RED, GPIO.LOW)
    time.sleep(0.4)

def green_indicate(speed):
    GPIO.output(GRN, GPIO.HIGH)
    time.sleep(speed)
    GPIO.output(GRN, GPIO.LOW)
    time.sleep(speed)

# Main loop
try:
    #init Ultrasonic
    pi = pigpio.pi() # Connect to local Pi.

    pi.set_mode(TRIGGER, pigpio.OUTPUT)
    pi.set_mode(ECHO, pigpio.INPUT)

    cb = pi.callback(ECHO, pigpio.EITHER_EDGE, cbfunc)

    GPIO.output(GRN, GPIO.HIGH)

    #motorPWMS
    pi.set_mode(EN1, pigpio.OUTPUT)
    pi.set_mode(EN2, pigpio.OUTPUT)
    pi.set_PWM_frequency(EN1, PWM_FREQ)
    pi.set_PWM_frequency(EN2, PWM_FREQ)

    #JSON SETUP
    f = open('/home/pi/Desktop/pothole.json')
    data = json.load(f)
    id = data['id']
    print(id)
    f.close()

    #Servo Setup
    pwm = setup_servo()
    time.sleep(2)
    set_servo_angle(pwm, 130)
    time.sleep(2)
    set_servo_angle(pwm, 50)
    time.sleep(0.5)
    print("srevo move")
    #GPS Setup
    print("gps")
    GPS=setup_GPS()
    print("gps succ")

    #Lights Setup
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GRN, GPIO.LOW)
    GPIO.output(WHT, GPIO.LOW)
    red_indicate()
    
    while True:
        #Forward Routineaa
        forward(85)
        pi.gpio_trigger(TRIGGER, 10)
        time.sleep(0.01)
        print(DIST)
        
        # Assuming a pothole depth threshold of 5 cm
        if DIST >= 6:
            #Stop Sequence
            stop()
            time.sleep(0.1)
            red_indicate()

            #Backward Sequence
            backward(100)    
            time.sleep(0.65)            
            stop()

            #First Img Capture Sequence
            GPIO.output(WHT, GPIO.HIGH)
            GPIO.output(RED, GPIO.HIGH)
            set_servo_angle(pwm,95)
            id+=1
            
            image_path1 = capture_image(id, 'a')
            print("Image Captured")
            GPIO.output(WHT, GPIO.LOW)
            GPIO.output(RED, GPIO.LOW)

            #2nd Image Position Sequence
            forward(100)
            time.sleep(0.55)
            stop()

            #second Img Capture Sequence
            GPIO.output(RED, GPIO.HIGH)
            GPIO.output(WHT, GPIO.HIGH)
            set_servo_angle(pwm,50)
            image_path2 = capture_image(id,'b')
            print("Image Captured")
            GPIO.output(WHT, GPIO.LOW)

            #Server Upload Sequence
            green_indicate(0.4)

            location = get_GPS(GPS)
            if location == "0,0":
                time.sleep(2)
                location=get_GPS(GPS)
                if location == "0,0":
                    time.sleep(4)
                    location=get_GPS(GPS)
            print(location)
                
            status_code = send_data_to_server(id,(DIST-4.0),location, image_path1, image_path2)
            if status_code == 200:
                print("Pothole detected and data sent successfully.")
                green_indicate(0.2)
                green_indicate(0.1)
            else:
                print("Failed to send data to server.")
                green_indicate(0.5)
                green_indicate(0.7)
            set_servo_angle(pwm,50)
            time.sleep(0.5)
            
            GPIO.output(RED, GPIO.LOW)
        
            #forward Sequence
            forward(85)
            time.sleep(1)
        #time.sleep(0.01)  # Adjust as needed for sampling frequency

except KeyboardInterrupt:
    GPIO.cleanup()
    cb.cancel() # Cancel callback.
    pi.stop() 

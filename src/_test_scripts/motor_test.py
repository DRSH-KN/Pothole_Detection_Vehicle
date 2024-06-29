import RPi.GPIO as GPIO
import time

IN1 = 20  # GPIO pin 20 for controlling one direction of the motor
IN2 = 21
IN3 = 7
IN4 = 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

def forward(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def backward(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)


try:
    while True:
        forward(100)
        time.sleep(3)
        backward(100)
        time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()

        


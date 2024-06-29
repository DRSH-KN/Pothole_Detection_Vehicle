import pigpio
import RPi.GPIO as GPIO
import time

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

pwm = setup_servo()
set_servo_angle(pwm, 130)
time.sleep(0.5)
set_servo_angle(pwm, 50)
time.sleep(0.5)
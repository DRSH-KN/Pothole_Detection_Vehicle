import RPi.GPIO as GPIO
import time
import requests
from picamera import PiCamera

# Initialize ultrasonic sensor
TRIG = 19
ECHO = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Initialize camera
camera = PiCamera()

# Function to measure distance using ultrasonic sensor
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    pulse_start = time.time()
    pulse_end = time.time()
    
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

# Function to capture image
def capture_image():
    image_path = "/home/pi/pothole_image.jpg"  # Set your desired image path
    camera.start_preview()
    time.sleep(2)  # Allow camera to warm up
    camera.capture(image_path)
    camera.stop_preview()
    return image_path

# Function to send data to server
def send_data_to_server(depth, image_path):
    url = "http://your_server_address/endpoint"
    files = {'photo': open(image_path, 'rb')}
    data = {'depth': depth}
    response = requests.post(url, files=files, data=data)
    return response.status_code

# Main loop
try:
    while True:
        distance = measure_distance()
        
        # Assuming a pothole depth threshold of 10 cm
        if distance < 10:
            image_path = capture_image()
            status_code = send_data_to_server(distance, image_path)
            if status_code == 200:
                print("Pothole detected and data sent successfully.")
            else:
                print("Failed to send data to server.")
        
        time.sleep(1)  # Adjust as needed for sampling frequency

except KeyboardInterrupt:
    GPIO.cleanup()

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
light = 6
GPIO.setup(light, GPIO.IN)
state = 0
while True:
    if GPIO.input(light):
        state = not state
        GPIO.output(led, state)
        

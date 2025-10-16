import r2r_dac as r2r
import signal_generator as sg
import time
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.OUT)
if __name__ == "__main__":
    try:
        DAC = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.14, True)

        while True:
            try:
                sg.get_sin_wave_amplitude(frequency, sg.wait_for_sampling_period(sampling_frequency))

    finally:
        dac.deinit()
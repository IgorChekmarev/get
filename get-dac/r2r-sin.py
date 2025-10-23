import r2r_dac as r2r
import signal_generator as sg
import time
amplitude = 3.14
signal_frequency = 10
sampling_frequency = 1000 
start_time = 0
if __name__ == "__main__":
    try:
        DAC = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.14, True)

        while True:
            try:
                end_time = time.time()
                elapsed_time = end_time-start_time
                a = sg.get_sin_wave_amplitude(signal_frequency, elapsed_time)
                DAC.set_voltage(amplitude*a)
                sg.wait_for_sampling_period(sampling_frequency)
            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        DAC.deinit()
import numpy as np
import time
import math
def get_sin_wave_amplitude(freq, time):
    return float(math.sin(2*math.pi*freq*time)+1)/2

def wait_for_sampling_period(sampling_frequency):

    time.sleep((1/sampling_frequency))



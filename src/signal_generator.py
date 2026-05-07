import numpy as np
def generate_sine_wave(freq=1, amp=1, phase=0, samples=1000):
    t = np.linspace(0, 1, samples)
    y = amp * np.sin(2 * np.pi * freq * t + phase)
    return t, y
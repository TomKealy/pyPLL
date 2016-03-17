import numpy as np
from scipy.signal import remez

time_step = 1/10000.0
time_end = 1.0
time = np.linspace(0.0, 1.0, 10000)
carrier_freq = 1000
carrier_phase = -0.8
recieved_signal = np.cos(4*np.pi*carrier_freq + 2*carrier_phase)
lpf_taps = 10
lpf_bands = [0.0, 0.01, 0.02, 0.04]
lpf_desired = [1, 1]
h = remez(lpf_taps, lpf_bands, lpf_desired)
mu = .003
fc = 1000
theta = np.zeros(10000)
lpf_buff = np.zeros(lpf_taps+1)
for k in range(len(time)-1):
    lpf_buff = [lpf_buff[1:lpf_taps+1], recieved_signal[k]*np.sin(4*np.pi*fc*time[k]+2*theta[k])]
    theta[k+1] = theta[k]-mu*np.fliplr(h)*np.conj(z)

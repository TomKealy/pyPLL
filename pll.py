import numpy as np

phase_offset = 0.5
freqequency_offset = 0.30
pll_bandwidth = 0.01
damping_factor = 0.707
pll_gain = 1000
num_samples = 100

t1 = pll_gain/(pll_bandwidth*pll_bandwidth)
t2 = (2*damping_factor)/pll_bandwidth

b0 = (4*pll_gain/t1)*(1.0+(t2/2.0))
b1 = (8*pll_gain/t1)
b2 = (4*pll_gain/t1)*(1.0-(t2/2.0))

a1 = -2.0
a2 = 1.0

v0 = 0.0
v1 = 0.0
v2 = 0.0

phi = phase_offset #input signals initial pahse
phi_hat = 0.0 #PLL initial pahse

ref = []
out = []
diff = []

for i in range(0, num_samples-1):
    x = np.exp(1j*phi)
    ref.append(x)
    phi += freqequency_offset

    y = np.exp(1j*phi_hat)
    out.append(y)
        
    delta_phi = np.angle(x*np.conj(y))
    diff.append(delta_phi)
    
    v2 = v1
    v1 = v0
    v0 = delta_phi - v1*a1 - v2*a2
    
    phi_hat = v0*b0 + v1*b1 +v2*b2

import matplotlib.pyplot as plt
plt.plot(out)
plt.show()

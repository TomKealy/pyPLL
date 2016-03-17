import numpy as np
import pdb


class LoopFilter(object):
    def __init__(self, gain, bandwidth, damping):
        self.a1 = -2.0
        self.a2 = 1.0
        t1 = gain/(bandwidth*bandwidth)
        t2 = (2*damping)/bandwidth
        self.b0 = (4*gain/t1)*(1.0+t2/2.0)
        self.b1 = (8*gain)/t1
        self.b2 = (4*gain/t1)*(1.0-t2/2.0)
        self.v0 = 0.0
        self.v1 = 0.0
        self.v2 = 0.0
        self.output = 0.0
        
    def advance_filter(self, phase_difference):
        self.v2 = self.v1
        self.v1 = self.v0
        self.v0 = (phase_difference - self.v1*self.a1 - self.v2*self.a2)

    def new_output(self):
        return self.v0*self.b0 + self.v1*self.b1 + self.v2*self.b2


class PLL(object):
    def __init__(self, lf_gain, lf_bandwidth, lf_damping):
        self.phase_estimate = 0.0
        self.vco = np.exp(1j*self.phase_estimate)
        self.phase_difference = 0.0
        self.loop_filter = LoopFilter(lf_gain, lf_bandwidth, lf_damping)
        
    def update_phase_estimate(self):
        self.phase_estimate = self.loop_filter.new_output()
        self.vco = np.exp(1j*self.phase_estimate)

    def update_phase_difference(self, in_sig):
        self.phase_difference = np.angle(in_sig*np.conj(self.vco))

    def step(self, in_sig):
        # Takes an instantaneous sample of a signal and updates the PLL's inner state
        self.update_phase_difference(in_sig)
        self.loop_filter.advance_filter(self.phase_difference)
        self.update_phase_estimate()

def main():
    import matplotlib.pyplot as plt
    pll = PLL(1000, 0.01, 0.707)
    num_samples = 500
    phi = 0.999999
    frequency_offset = 0.3
    ref = []
    out = []
    diff = []
    for i in range(0, num_samples - 1):
        in_sig = np.exp(1j*phi)
        phi += frequency_offset
        pll.step(in_sig)
        ref.append(in_sig)
        out.append(pll.vco)
        diff.append(pll.phase_difference)
    #plt.plot(ref)
    plt.plot(ref)
    plt.plot(out)
    plt.plot(diff)
    plt.show()

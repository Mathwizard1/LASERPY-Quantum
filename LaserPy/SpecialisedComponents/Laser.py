class Laser:
    """
    Laser class for simulations
    """

    def __init__(self, name, fr_freq=0, N0=N_transparent, S0= err_fault, Phi0= err_fault):
        self.name = name
        self.N0 = N0
        self.S0 = S0
        self.Phi0 = Phi0

        self.ideal_freq = fr_freq
        """
        ideal frequency
        """

        self.fr_freq = fr_freq
        """
        free running frequency
        """

        self.N_t = self.N0
        """
        Number of Carriers
        """

        self.S_t = self.S0
        """
        Photon density
        """

        self.Phi_t = self.Phi0
        """
        Optical phase
        """

        self.dPhi = 0
        """
        Stored instantaneous delta phase change
        """

        self.E_t = 0
        """
        Laser Optical field (complex)
        """
    
    def values(self):
        """
        Physical constraint check and get simulation values
        """
        self.N_t = max(err_fault, self.N_t)
        self.S_t = max(err_fault, self.S_t)

        # Phase and Photons gives Optical field
        self.E_t = np.sqrt(Power(self.S_t, self.fr_freq)) * np.exp2(1j * self.Phi_t)

        return (self.N_t, self.S_t, self.Phi_t, self.E_t)

    def reset(self):
        """
        Reset all data
        """
        self.N_t = self.N0
        self.S_t = self.S0
        self.Phi_t = self.Phi0

        self.dPhi = 0
        self.E_t = 0

    def update(self, I_t, t, dt, Fn_t= 0.0, Fs_t= 0.0, Fphi_t= 0.0):
        """
        Update N, S, phi and return current value
        """
        temp_N_t = self.N_t + self.dN_dt(I_t, Fn_t) * dt 
        temp_S_t = self.S_t + self.dS_dt(Fs_t) * dt
        self.dPhi = self.dPhi_dt(Fphi_t) * dt

        """ time step update """ 
        self.N_t = temp_N_t
        self.S_t = temp_S_t
        self.Phi_t += self.dPhi

        return self.values()

    def dN_dt(self, I_t, Fn_t):
        """
        delta Number of Carriers
        """
        val = I_t / (universalConstants.charge.value * Vol) - self.N_t / Tau_n - g * ((self.N_t - self.N0) / (1.0 + Epsilon * self.S_t)) * self.S_t + Fn_t
        return val

    def dS_dt(self, Fs_t):
        """
        delta Photon density
        """
        val = Gamma_cap * g * ((self.N_t - self.N0) / (1.0 + Epsilon * self.S_t)) * self.S_t - self.S_t / Tau_p + Gamma_cap * Beta * self.N_t / Tau_n + Fs_t
        return val

    def dPhi_dt(self, Fphi_t):
        """
        delta Optical phase
        """
        val = (Alpha / 2.0) * (Gamma_cap * g * (self.N_t - self.N0) - 1.0 / Tau_p) + Fphi_t
        return val
        
master_laser = Laser("Master", Laser_freq)
master_current = CurrentDriver()
master_current.set_Modulation(None, t_unit)
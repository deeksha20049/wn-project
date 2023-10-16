import numpy as np

class WiFiAccessPoint:
    def __init__(self, ap_id, ap_position, transmit_power, noise_psd, bandwidth,sigma):
        self.ap_id = ap_id
        self.ap_position = ap_position
        self.transmit_power = transmit_power
        self.noise_psd = noise_psd
        self.bandwidth = bandwidth
        self.sigma = sigma
        
    #standard Rayleigh distribution
    def calculate_channel_gain_rayleigh(self,k):
        X0 = np.exp(1j * np.radians(45))
        X1 = np.random.normal(0, 1) + 1j * np.random.normal(0, 1)
        H = np.sqrt(k / (k + 1)) * X0 + np.sqrt(1 / (k + 1)) * X1
        return np.abs(H)
    
    def calculate_distance(self, user_position):
        user_position = np.array(user_position)
        return np.linalg.norm(np.array(user_position) - np.array(self.ap_position))
    
    def calculate_channel_gain(self, user, fc):
        distance = self.calculate_distance(user.position)
        dref = 5.0  # Breakdown distance, d_BP (in meters)
        free_space_path_loss = 20 * np.log10(fc * distance) - 147.5

        #path loss calculation
        if distance <= dref:
            shadow_fading = np.random.normal(0, 2) # std. dev. is 3dB  
            path_loss = free_space_path_loss + shadow_fading
            H =  self.calculate_channel_gain_rayleigh(1)
        else:
            shadow_fading = np.random.normal(0, 3.16) # std. dev. is 6dB
            path_loss = free_space_path_loss + 35*np.log10(distance/dref) + shadow_fading   
            H =  self.calculate_channel_gain_rayleigh(0)        
        channel_gain = (H**2) * (10 ** (-path_loss/10))
        return channel_gain

    def calculate_snr(self, channel_gain):
        return (channel_gain * self.transmit_power) / (self.noise_psd * self.bandwidth)


if __name__ == "__main__":
    # Simulation parameters
    fc = 2.4e9  # Central carrier frequency (2.4 GHz in Hz)
    # WiFi channel gain parameters
    shadow_fading_std_dev = 10  # Standard deviation of shadow fading (in dB)
    # Free-space path loss parameters
    reference_distance = 10.0  # dref (in meters)
    path_loss_exponent = 2.75  # Path loss exponent

    # WiFi SNR parameters
    wifi_transmit_power = 1e-3 * 10**(20/10)  # Transmit power of the WiFi AP (in Watts)
    wifi_noise_psd = 10**(-174/10)  # PSD of noise at the receiver (in A^2/Hz)
    wifi_bandwidth = 20e6  # WiFi system bandwidth (in Hz)

    # Simulation parameters for users and AP
    ap_position = (0, 0)  # AP position (x, y) in the room

    # Update WiFi access point creation with the updated parameters
    wifi_ap = WiFiAccessPoint(ap_id=1, ap_position=ap_position, transmit_power=wifi_transmit_power, noise_psd=wifi_noise_psd, bandwidth=wifi_bandwidth, sigma=shadow_fading_std_dev)

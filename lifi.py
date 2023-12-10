import numpy as np
from typing import List
import json 

class LifiAccessPoint:
    def __init__(self, x, y, Φ_1by2=60, Apd=100*1e-4, ref_index=1.5, FOV=90, gf=1,
            room_x=5, room_y=5, room_z=5, h=0.8, Rpd=0.53, pw=0.8, Popt=3, k=3, Nlifi=1e-21, Blifi=20*1e6):
        # attribute for Half-intensity radiation angle (Φ1/2)
        self.Φ_1by2 = Φ_1by2 * np.pi / 180
        self.m = -np.log(2) / np.log(np.cos(np.radians(Φ_1by2)))
        # Refractive ref_index of the medium
        self.ref_index = ref_index
        # FoV semi-angle of PD, Ψmax
        self.FOV = FOV * np.pi / 180
        # physical area of the PD, Apd
        self.Apd = Apd
        # gain of the optical filter, gf
        self.gf = gf
        # length of the room in the x-direction (horizontal) in meters.
        self.room_x = room_x
        # length of the room in the y-direction (vertical) in meters.
        self.room_y = room_y
        # height of the room in meters
        self.room_z = room_z
        # height of the user above the receiver plane
        self.h = h
        # position of the lifi access point in ceiling
        self.lifi_position = np.array([x, y, room_z])
        # Detector responsivity, Rpd
        self.Rpd = Rpd
        # Transmitted optical power per LiFi AP, Popt
        self.Popt = Popt
        # optical to electrical conversion coefficient, k
        self.k = k
        # PSD of noise in LiFi AP, NLiFi
        self.Nlifi = Nlifi
        # Bandwidth of LiFi AP, BLiFi
        self.Blifi = Blifi
        # Wall reflectivity, pw
        self.pw = pw
        
        # Number of points in the x and y directions
        # self.Nx = int(room_x * 10)
        # self.Ny = int(room_y * 10)
        # self.x = np.linspace(0, room_x, self.Nx)
        # self.y = np.linspace(0, room_y, self.Ny)
        # self.XR, self.YR = np.meshgrid(self.x, self.y)
        # print(self.XR)
        # print(self.XR.shape)
        import os
        print(os.getcwd())
        name = "./channel_gain_nlos_mids_"+str(int(self.lifi_position[0]*100)) +"_"+ str(int(self.lifi_position[1]*100))
        with open(name+'.json') as json_file:
            self.channel_gain_nlos_data = json.load(json_file)
        # for i,j in self.channel_gain_nlos.items():
        #     self.channel_gain_nlos[i] = np.array(j)
    def get_channel_gain(self, user_x, user_y):
        # uncomment this line to include NLOS channel gain
        return self.channel_gain_los(user_x, user_y) #+ self.channel_gain_nlos(user_x, user_y)

    def channel_gain_los(self, user_x, user_y):
        d = self.distance(user_x, user_y)        
        # both angles are equal due to symmetry
        incidence = self.angle_incidence(user_x, user_y)
        irradiance = incidence           
        gc = self.optical_gain(incidence)
        channel_gain = ((self.m + 1) * self.Apd * (np.cos(irradiance)**self.m) * np.cos(incidence) * self.gf * gc) / (2 * np.pi * (d**2))
        # print(incidence, irradiance, channel_gain, self.m, gc, self.Apd, self.gf)
        return channel_gain
    
    
    def custom_round(self,number):
        rounded_number = round(number, 1)
    
    # Set the second decimal place to 5
        modified_number = rounded_number + 0.05
        rounded_number = round(modified_number, 2)
        return rounded_number if rounded_number <= 5 else rounded_number - 0.1
    
    def channel_gain_nlos(self, user_x, user_y):
        # boxes_per_meter = 10
        # dl, dh = 1/boxes_per_meter, 1/boxes_per_meter
        # height_coord = np.arange(self.h, self.room_z, dh)
        # length_coord = np.arange(self.h, self.room_x, dl)
        # user_position = np.array([user_x, user_y, self.h])
        # integration = 0
        
        # for height in height_coord:
        #     # print(f'{height:.3f}  ')
        #     for length in length_coord:
        #         locations = [np.array([length, 0, height]), np.array([length, self.room_y, height]),
        #                     np.array([0, length, height]), np.array([self.room_x, length, height])]
        #         for curr_location in locations:
        #             d_iw = np.linalg.norm(curr_location - self.lifi_position)
        #             d_wu = np.linalg.norm(user_position - curr_location)
        #             theta_iw = np.arccos((self.room_z - height) / d_iw)
        #             ϑ_iw = 90 - theta_iw
        #             phi_wu = np.arccos((height - self.h) / d_wu)
        #             ϑ_wu = 90 - phi_wu
        #             numerator = (self.m + 1) * self.Apd * self.pw * (np.cos(theta_iw)**self.m) * \
        #                         self.gf * self.optical_gain(phi_wu) * np.cos(phi_wu) * np.cos(ϑ_iw) * np.cos(ϑ_wu)
        #             integration += (numerator * dl * dh) / (2 * (np.pi * d_iw * d_wu)**2)
        # return integration
        # Read files
        # floor or ceil the value of user_x and user_y to _._0 or _._5
        user_x = round(self.custom_round(user_x), 2)
        user_y = round(self.custom_round(user_y), 2)
        
        return self.channel_gain_nlos_data[str(tuple([user_x, user_y]))]
        
    
    def signal_to_noise_ratio(self, user_x, user_y, otherLifiAPs:List=None):
        summation_term = 0
        # for lifi in otherLifiAPs:
            # print(f'Lifi at {lifi.lifi_position} has gain', lifi.get_channel_gain(user_x, user_y))
            # summation_term += (lifi.Rpd * lifi.get_channel_gain(user_x, user_y) * lifi.Popt / lifi.k) ** 2
        # print('self gain: ', self.get_channel_gain(user_x, user_y))
        numerator = (self.Rpd * self.get_channel_gain(user_x, user_y) * self.Popt / self.k) ** 2
        # uncomment this line to include noise from other LiFi APs
        denominator = self.Nlifi * self.Blifi + summation_term 
        # print(f'numerator: {numerator}, denominator: {denominator}, sum: {summation_term}')   
        return numerator / denominator
    
    
    def signal_to_noise_ratio_nlos(self, user_x, user_y, otherLifiAPs:List=None):
        numerator = (self.Rpd * self.channel_gain_nlos(user_x, user_y) * self.Popt / self.k) ** 2
        denominator = self.Nlifi * self.Blifi  
        return numerator / denominator
    
    def distance(self, user_x, user_y):
        user_position = np.array([user_x, user_y, self.h])
        distance =  np.linalg.norm(user_position - self.lifi_position)
        return distance
    
    def optical_gain(self, angle_incidence):
        if 0 <= angle_incidence <= self.FOV:
            return (self.ref_index**2) / (np.sin(self.FOV)**2)
        else:
            return 0
    
    def angle_incidence(self, user_x, user_y):
        d = self.distance(user_x, user_y)
        return np.arccos((self.room_z - self.h) / d)


if __name__ == "__main__":
    x, y = 1.25, 1.25
    lifi_ap1 = LifiAccessPoint(x=1.25, y=1.25)
    print(lifi_ap1.channel_gain_nlos(1.37, 2.13))
    # lifi_ap2 = LifiAccessPoint(x=1.25, y=3.75)
    # lifi_ap3 = LifiAccessPoint(x=3.75, y=3.75)
    # lifi_ap4 = LifiAccessPoint(x=3.75, y=1.25)

    # ang_incidence = lifi_ap1.angle_incidence(x, y)
    # optical_gain = lifi_ap1.optical_gain(ang_incidence)
    # # print(ang_incidence)
    # # print(optical_gain)
    # # H = lifi_ap1.get_channel_gain(x, y)
    
    # print('Location: ', 0, 0)
    # snr = lifi_ap1.signal_to_noise_ratio(0, 0, otherLifiAPs=[lifi_ap2, lifi_ap3, lifi_ap4])
    # print(snr)
    # print('Location: ', 1.25, 1.25)
    # snr = lifi_ap1.signal_to_noise_ratio(1.2, 1.2, otherLifiAPs=[lifi_ap2, lifi_ap3, lifi_ap4])
    # print(snr)

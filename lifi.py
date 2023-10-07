import numpy as np

class LifiAccessPoint:
    def __init__(self, x, y, Φ_1by2=60, Apd=1e-4, ref_index=1.5, FOV=90, gf=1,
                P_total=20, room_x=5, room_y=5, room_z=5, h=0.8):
        # attribute for Half-intensity radiation angle (Φ1/2)
        self.Φ_1by2 = Φ_1by2 * np.pi / 180
        self.m = -np.log(2) / np.log(np.cos(np.radians(Φ_1by2)))
        # Refractive ref_index of the medium
        self.ref_index = ref_index
        # FoV semi-angle of PD, Ψmax
        self.FOV = FOV * np.pi / 180
        self.G_Con = (ref_index**2) / np.sin(self.FOV)
        # physical area of the PD, Apd
        self.Apd = Apd
        # gain of the optical filter, gf
        self.gf = gf
        # total optical power transmitted by the LED, P_total
        self.P_total = P_total
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
        
        # Number of points in the x and y directions
        self.Nx = int(room_x * 10)
        self.Ny = int(room_y * 10)
        self.x = np.linspace(0, room_x, self.Nx)
        self.y = np.linspace(0, room_y, self.Ny)
        self.XR, self.YR = np.meshgrid(self.x, self.y)

    def get_channel_gain(self, user_x, user_y):
        d = self.distance(user_x, user_y)
        incidence = self.angle_incidence(user_x, user_y)
        gc = self.optical_gain(incidence)
        irradiance = incidence   # both angles are equal due to symmetry
        channel_gain = ((self.m + 1) * self.Apd * (np.cos(irradiance)**self.m) * np.cos(incidence) * \
                        self.gf * gc) / (2 * np.pi * d**2)
        return channel_gain
        # P_rec = self.P_total * H * self.gf * self.G_Con
        # P_rec_dBm = 10 * np.log10(P_rec)
        # return P_rec_dBm
    
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
    x, y = 1, 1
    lifi_ap = LifiAccessPoint(x = x, y = y)
    d = lifi_ap.distance(x, y)
    ang_incidence = lifi_ap.angle_incidence(x, y)
    optical_gain = lifi_ap.optical_gain(ang_incidence)
    H = lifi_ap.get_channel_gain(x, y)
    print(d)
    print(ang_incidence)
    print(optical_gain)
    print(H)

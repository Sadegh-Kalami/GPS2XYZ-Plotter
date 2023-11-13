import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class GPSPlotter:
    def __init__(self, plotter_type='2D',mull = 45 ):
        self.PLOTTER = plotter_type
        self.mull = 45

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        r = 6371  # radius of the Earth in kilometers
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)

        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = r * c
        return d

    @staticmethod
    def latlon_to_xyz(lat, lon):
        r = 6371  # https://en.wikipedia.org/wiki/Earth_radius
        theta = math.pi / 2 - math.radians(lat)
        phi = math.radians(lon)
        x = r * math.sin(theta) * math.cos(phi)  # bronstein (3.381a)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)
        return [x, y, z]

    @staticmethod
    def GPS2XYZ(path, n):
        data = pd.read_csv(path)
        x = []
        y = []
        z = []
        lat1 = data['Latitude'].iloc[:]
        lon1 = data['Longitude'].iloc[:]

        for i in range(n):
            XYZ = GPSPlotter.latlon_to_xyz(lat1[i], lon1[i])
            x.append(XYZ[0])
            y.append(XYZ[1])
            z.append(XYZ[2])

        x = list(map(lambda xi: (xi - x[0]) * 1000, x))
        y = list(map(lambda yi: (yi - y[0]) * 1000, y))
        z = list(map(lambda zi: (zi - z[0]) * 1000, z))

        return x, y, z

    def plot(self, data_slam, x_GPS, y_GPS, z_GPS):
        datax = data_slam[:, 0]
        datay = data_slam[:, 1]
        dataz = data_slam[:, 2]


        if self.PLOTTER == '2D':
            plt.plot(datax * self.mull, datay * self.mull, c='b', label='ORBSLAM3 Trajectory')
            plt.plot(x_GPS, y_GPS, c='r', label='GPS Data')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.legend()
            plt.show()

        elif self.PLOTTER == '3D':
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(datax * 100, datay * 100, dataz * 100, c='b', label='ORBSLAM3 Trajectory')
            ax.plot(x_GPS, y_GPS, z_GPS, c='r', marker='*', label='GPS Data')
            ax.set_xlabel('X Label')
            ax.set_ylabel('Y Label')
            ax.set_zlabel('Z Label')
            ax.legend()
            plt.show()


if __name__ == "__main__":
    plotter = GPSPlotter('2D',mull=45)#'2D' or '3D'
    path = 'GPS_data.csv'  # PATH TO GPS DATA
    x_GPS, y_GPS, z_GPS = plotter.GPS2XYZ(path, 1255)
    data_slam = np.loadtxt('total_xyz.txt')
    plotter.plot(data_slam, x_GPS, y_GPS, z_GPS)

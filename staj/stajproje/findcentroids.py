from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans2, whiten
from scipy.cluster.vq import vq, kmeans, whiten
from kneed import DataGenerator, KneeLocator
import math
import time
import os
import sys
from ctypes import *
from math import radians, cos, sin, asin, sqrt

class Point(object):
    '''Creates a point on a coordinate plane with values x and y.'''

    COUNT = 0

    def __init__(self, x, y):
        '''Defines x and y variables'''
        self.x = x
        self.y = y

    def distance_to_line(self, p1, p2):
        x_diff = p2.x - p1.x
        y_diff = p2.y - p1.y
        num = abs(y_diff * self.x - x_diff * self.y + p2.x * p1.y - p2.y * p1.x)
        den = math.sqrt(y_diff ** 2 + x_diff ** 2)
        return num / den


def latbul(satir):

    liste = satir.split(",")
    latt=liste[0]
    return latt


def longbul(satir):

    liste = satir.split(",")
    long = liste[1]
    return long
def time(satir):

    liste = satir.split(",")
    a=liste[2]
    a=a.replace(" ","")
    time = a+","+liste[3]
    return time
def timee(satir):

    liste = satir.split(",")

    bb = liste[4]
    bb = bb.replace(" ", "")
    time = bb+","+liste[5]
    return time
def maxbul(array):
    max=0
    for i in range(len(array)):
        if array[i]>max:
            max=array[i]
            k=i
    return k+1


def findk(distortions,rangemax):
    distances = []
    for i in range(len(distortions)):
        p1 = Point(1, distortions[0])
        p2 = Point(rangemax, distortions[distortions.__len__() - 1])
        p = Point(i + 1, distortions[i])
        distances.append(p.distance_to_line(p1, p2))
    k=maxbul(distances)
    return k

def main():
    for dirname, dirnames, filenames in os.walk('StayPoint'):
        filenum = len(filenames)
        for filename in filenames:
            if filename.endswith('plt'):
                gpsfile = os.path.join(dirname, filename)
                with open(gpsfile, "r") as file:
                    stayliste = []
                    for i in file:
                        staya = i[1:-2]
                        staya = staya.replace('\'', "")
                        stayliste.append(staya)
                        tiimee=[]
                        tiime = []
                        staylat = []
                        staylong = []

                    for i in stayliste:
                        staylat.append(float(latbul(i)))
                        staylong.append(float(longbul(i)))
                        tiime.append(str(time(i)))
                        tiimee.append(str(timee(i)))
                x3 = [staylat[0], staylong[0]]

                pointlen = staylat.__len__()
                count = 1

                while count < pointlen:
                    x3 = np.vstack((x3, (staylat[count], staylong[count])))
                    count += 1

                # create new plot and data
                plt.plot()
                X = np.array(list(zip(staylat, staylong))).reshape(len(staylat), 2)
                colors = ['b', 'g', 'r']
                markers = ['o', 'v', 's']

                # k means determine k
                distortions = []

                rangemax = 15

                if pointlen < 15:
                    rangemax = pointlen

                K = range(1, rangemax)
                for k in K:
                    kmeanModel = KMeans(n_clusters=k).fit(X)
                    kmeanModel.fit(X)
                    distortions.append(
                        sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])
                optimumk = findk(distortions,rangemax)

                x, y = kmeans2(x3, optimumk, iter=1520)

                count = x.__len__()

                sonuc = []
                K = range(0, count)
                for k in K:
                    Y = range(0, staylat.__len__())
                    fark = 1000
                    for y in Y:
                        m = float(x[k, 0]) - float(staylat[y])
                        mm = float(x[k, 1]) - float(staylong[y])
                        m = m * m
                        mm = mm * mm
                        f = mm + m
                        m = math.sqrt(f)
                        if m < fark:
                            fark = m
                            index = y
                    sonuc.append(index)
                    centerlat = []
                    centerlong = []
                    centertime = []
                    centertimee = []
                    sonucc = sorted(sonuc)

                    count = sonucc.__len__()
                    K = range(0, count)
                    for k in K:
                        centerlat.append(staylat[sonucc[k]])
                        centerlong.append(staylong[sonucc[k]])
                        centertime.append(tiime[sonucc[k]])
                        centertimee.append(tiimee[sonucc[k]])


                    count = centerlong.__len__()
                    centroids = []
                    add = str(centerlat[0]),str(centerlong[0]),str(centertime[0]),str(centertimee[0])
                    centroids.append(add)

                    pointlen = centerlat.__len__()
                    count = 1

                    while count < pointlen:
                        add=str(centerlat[count]),str(centerlong[count]),centertime[count],centertimee[count]
                        centroids.append(add)
                        count += 1


                    if len(centroids) > 0:
                        spfile = gpsfile.replace('StayPoint', 'CentroidsPoint')
                        if not os.path.exists(os.path.dirname(spfile)):
                            os.makedirs(os.path.dirname(spfile))

                        spfile_handle = open(spfile, 'w+')


                        for sp in centroids:
                            b = str(sp)
                            spfile_handle.write(b + "\n")

                        spfile_handle.close()
if __name__ == '__main__':
    main()
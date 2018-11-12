import time
import os
import sys
from ctypes import *
from math import radians, cos, sin, asin, sqrt


time_format = '%Y-%m-%d,%H:%M:%S'

def distance(a, b):
    return  sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def point_line_distance(point, start, end):
    if (start == end):
        return distance(point, start)
    else:
        n = abs(
            (end[0] - start[0]) * (start[1] - point[1]) - (start[0] - point[0]) * (end[1] - start[1])
        )
        d = sqrt(
            (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
        )
        return n / d

def rdp(points, epsilon):
    """
    Reduces a series of points to a simplified version that loses detail, but
    maintains the general shape of the series.
    """
    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d
    if dmax >= epsilon:
        results = rdp(points[:index+1], epsilon)[:-1] + rdp(points[index:], epsilon)
    else:
        results = [points[0], points[-1]]
    return results



def latbul(satir):

    liste = satir.split(",")
    latt=liste[0]
    return latt


def longbul(satir):

    liste = satir.split(",")
    long = liste[1]
    return long
def time(satir):
    liste=satir.split(",")
    time=liste[5]
    return time

def hour(satir):
    liste=satir.split(",")
    hour=liste[6]
    return hour
def manuel(satir):
    liste=satir.split(",")
    manuel=liste[2]
    return manuel
def foot(satir):
    liste=satir.split(",")
    foot=liste[3]
    return foot
def km(satir):
    liste=satir.split(",")
    km=liste[4]
    return km


def main():
    for dirname, dirnames, filenames in os.walk('Data'):
        for filename in filenames:
            if filename.endswith('plt'):
                gpsfile = os.path.join(dirname, filename)
                with open(gpsfile, "r") as file:
                    file = file.readlines()[6:]
                    min=file.__len__()
                    if min>50:
                        liste = []
                        for i in file:
                            liste.append(i)

                        points = []
                        for i in liste:
                            points.append(
                                [float(latbul(i)), float(longbul(i)), str(manuel(i)), str(foot(i)), str(km(i)),
                                 str(time(i)), str(hour(i))])
                        tolerans=0.00005
                        b = rdp(points, tolerans)
                        line = b.__len__()
                        if b.__len__()<100:
                            b=points
                            line=b.__len__()

                        while line>700:
                            tolerans=tolerans+0.00005
                            b=rdp(b,(tolerans))
                            line=b.__len__()

                        spfile = gpsfile.replace('Data', 'Data_Processing')
                        if not os.path.exists(os.path.dirname(spfile)):
                            os.makedirs(os.path.dirname(spfile))

                        spfile_handle = open(spfile, 'w+')
                        say = 0
                        while say < line:
                            a = b[say][0]
                            aa = b[say][1]
                            bb = b[say][5]
                            bbb = b[say][6]
                            f = b[say][2]
                            ff = b[say][3]
                            fff = b[say][4]
                            spfile_handle.write(str(a))
                            spfile_handle.write(",")
                            spfile_handle.write(str(aa))
                            spfile_handle.write(",")
                            spfile_handle.write(str(f))
                            spfile_handle.write(",")
                            spfile_handle.write(str(ff))
                            spfile_handle.write(",")
                            spfile_handle.write(str(fff))
                            spfile_handle.write(",")
                            spfile_handle.write(str(bb))
                            spfile_handle.write(",")
                            spfile_handle.write(str(bbb))
                            # dosya.write("\n")
                            say += 1
                        spfile_handle.close()


if __name__ == '__main__':
    main()
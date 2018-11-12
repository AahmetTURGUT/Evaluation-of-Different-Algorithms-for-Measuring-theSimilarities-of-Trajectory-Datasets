#!/usr/bin/env python
# -*- coding: utf-8 -*-

# extract stay points from a GPS log file
# implementation of algorithm in
# [1] Q. Li, Y. Zheng, X. Xie, Y. Chen, W. Liu, and W.-Y. Ma, "Mining user similarity based on location history", in Proceedings of the 16th ACM SIGSPATIAL international conference on Advances in geographic information systems, New York, NY, USA, 2008, pp. 34:1--34:10.

import time
import os
import sys
from ctypes import *
from math import radians, cos, sin, asin, sqrt

time_format = '%Y-%m-%d,%H:%M:%S'


# structure of stay point
class stayPoint(Structure):
    _fields_ = [
        ("longitude", c_double),
        ("laltitude", c_double),
        ("arrivTime", c_uint64),
        ("leaveTime", c_uint64)
    ]


# calculate distance between two points from their coordinate
def getDistance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    m = 6371000 * c
    return m


def computMeanCoord(gpsPoints):
    lon = 0.0
    lat = 0.0
    for point in gpsPoints:
        fields = point.rstrip().split(',')
        lon += float(fields[0])
        lat += float(fields[1])
    return (lon / len(gpsPoints), lat / len(gpsPoints))


# extract stay points from a GPS log file
# input:
#        file: the name of a GPS log file
#        distThres: distance threshold
#        timeThres: time span threshold
# default values of distThres and timeThres are 200 m and 30 min respectively, according to [1]

def stayPointExtraction(file, distThres=200, timeThres= 60):
    stayPointList = []
    log = open(file, 'r')
    points = log.readlines()[6:]  # first 6 lines are useless
    pointNum = len(points)
    i = 0
    while i < pointNum:
        j = i + 1
        while j < pointNum:
            field_pointi = points[i].rstrip().split(',')
            field_pointj = points[j].rstrip().split(',')
            dist = getDistance(float(field_pointi[0]), float(field_pointi[1]),
                               float(field_pointj[0]), float(field_pointj[1]))

            if dist > distThres:
                t_i = time.mktime(time.strptime(field_pointi[-2] + ',' + field_pointi[-1], time_format))
                t_j = time.mktime(time.strptime(field_pointj[-2] + ',' + field_pointj[-1], time_format))
                deltaT = t_j - t_i
                if deltaT > timeThres:
                    sp = stayPoint()
                    sp.laltitude, sp.longitude = computMeanCoord(points[i:j + 1])
                    sp.arrivTime, sp.leaveTime = int(t_i), int(t_j)
                    stayPointList.append(sp)
                break
            j += 1
        # Algorithm in [1] lacks following line
        i = j
    return stayPointList

def morestayPointExtraction(file, distThres=20, timeThres= 10):
    stayPointList = []
    log = open(file, 'r')
    points = log.readlines()[6:]  # first 6 lines are useless
    pointNum = len(points)
    i = 0
    while i < pointNum:
        j = i + 1
        while j < pointNum:
            field_pointi = points[i].rstrip().split(',')
            field_pointj = points[j].rstrip().split(',')
            dist = getDistance(float(field_pointi[0]), float(field_pointi[1]),
                               float(field_pointj[0]), float(field_pointj[1]))

            if dist > distThres:
                t_i = time.mktime(time.strptime(field_pointi[-2] + ',' + field_pointi[-1], time_format))
                t_j = time.mktime(time.strptime(field_pointj[-2] + ',' + field_pointj[-1], time_format))
                deltaT = t_j - t_i
                if deltaT > timeThres:
                    sp = stayPoint()
                    sp.laltitude, sp.longitude = computMeanCoord(points[i:j + 1])
                    sp.arrivTime, sp.leaveTime = int(t_i), int(t_j)
                    stayPointList.append(sp)
                break
            j += 1
        # Algorithm in [1] lacks following line
        i = j
    return stayPointList
def main():
    for dirname, dirnames, filenames in os.walk('Data_Processing'):
        filenum = len(filenames)
        for filename in filenames:
            if filename.endswith('plt'):
                gpsfile = os.path.join(dirname, filename)
                spt = stayPointExtraction(gpsfile)
                if spt.__len__()<6:
                    spt = morestayPointExtraction(gpsfile)
                if len(spt) > 0:
                    spfile = gpsfile.replace('Data_Processing', 'StayPoint')
                    if not os.path.exists(os.path.dirname(spfile)):
                        os.makedirs(os.path.dirname(spfile))

                    spfile_handle = open(spfile, 'w+')

                    for sp in spt:
                        a = (str(sp.laltitude), str(sp.longitude), str(time.strftime(time_format, time.localtime(
                            sp.arrivTime))), str(time.strftime(time_format, time.localtime(sp.leaveTime))) )
                        b=str(a)
                        spfile_handle.write(b+"\n")

                    spfile_handle.close()



if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-

__author__ = 'Imawaka Hiroki (Kitagawa Lab) < u801286h@ecs.osaka-u.ac.jp >'

import numpy as np
from scipy.optimize import curve_fit

def CurveFitting(function, initial_param, data):
    '''
    実際にフィッティングを行う関数
    '''
    popt, pcov = curve_fit(function, data[:,0], data[:,1], p0=initial_param)
    perr = np.sqrt(np.diag(pcov))
    return popt, pcov, perr

def SaturationCurve(x, a, b):
    return a * np.exp(-x/b)

def InversionCurve(x, a, b, c):
    return a * np.exp(-x/b) + c

def BuildUpCurve(x, a, b):
    return a * (1 - np.exp(-x/b))

def Rabi(x, a, b, c):
    return a * np.exp(-x/b) * np.sin(np.radians(c*x))

def Ndegree(degree):
    def x(x, *args):
        if degree == 1:
            return args[0] * x + args[1]
        elif degree == 2:
            return args[0] * (x**2) + args[1] * x + args[2]
        elif degree == 3:
            return args[0] * (x**3) + args[1] * (x**2) + args[2] * x + args[3]
        elif degree == 4:
            return args[0] * (x**4) + args[1] * (x**3) + args[2] * (x**2) + args[3] * x + args[4]
        elif degree == 5:
            return args[0] * (x**5) + args[1] * (x**4) + args[2] * (x**3) + args[3] * (x**2) + args[4] * x + args[5]
        elif degree == 6:
            return args[0] * (x**6) + args[1] * (x**5) + args[2] * (x**4) + args[3] * (x**3) + args[4] * (x**2) + args[5] * x + args[6]
    return x

def Gaussian(x, a, b):
    return np.exp(-((x-b)**2)/(2*(a**2)))/np.sqrt(2*np.pi*(a**2))

def Sin(x, a, b, c, d):
    return a * np.sin(np.radians(b*x + c)) + d

def calcurate_sqrt_of_MSE(cf, data, degree, pops):
    '''
    2乗平均誤差(MSE)の平方根をだす
    '''
    if cf == 5:
        return
    sum = 0
    if cf == 0:
        for i in range(len(data)):
            sum += (SaturationCurve(data[i, 0], *pops) - data[i, 1])**2
    elif cf == 1:
        for i in range(len(data)):
            sum += (InversionCurve(data[i, 0], *pops) - data[i, 1])**2
    elif cf == 2:
        for i in range(len(data)):
            sum += (BuildUpCurve(data[i, 0], *pops) - data[i, 1])**2
    elif cf == 3:
        for i in range(len(data)):
            sum += (Rabi(data[i, 0], *pops) - data[i, 1])**2
    elif cf == 4:
        for i in range(len(data)):
            sum += (Ndegree(degree)(data[i, 0], *pops) - data[i, 1])**2
    return np.sqrt(sum/len(data))

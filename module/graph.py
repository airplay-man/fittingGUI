# -*- coding: utf-8 -*-

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

COLORdict = matplotlib.colors.cnames
COLORS = list(COLORdict.keys())

def plot_scatterdata(ax, data, settings, label):
    '''
    散布図の描画
    '''
    ax.plot(data[:,0], data[:,1], markersize=settings[2], marker=settings[1], linestyle=settings[3], linewidth=settings[4], color=COLORdict[settings[0]], zorder=3, label=label)

def plot_fittingresult(ax, xdata, ydata, fittingsettings):
    '''
    フィッティング結果を表示する部分だけ抜き出したもの
    '''
    ax.plot(xdata, ydata, color=COLORdict[fittingsettings[0]], linestyle=fittingsettings[1], linewidth=fittingsettings[2], zorder=1)

def plot_legend(ax, legendsettings, fontsettings):
    '''
    凡例の描画
    '''
    if legendsettings[0].get():
        if legendsettings[2] == '':
            ax.legend(numpoints=1, ncol=legendsettings[3], fontsize=fontsettings[1], markerscale=legendsettings[4])
        else:
            ax.legend(numpoints=1, loc=legendsettings[1], bbox_to_anchor=legendsettings[2], ncol=legendsettings[3], fontsize=fontsettings[1])

def set_axissettings(ax, fontsettings, xlabel, ylabel, xunit, yunit, xstart, ystart, xend, yend):
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax.tick_params(axis='x', which='major', labelsize=int(fontsettings[2]))
    ax.tick_params(axis='y', which='major', labelsize=int(fontsettings[2]))
    ax.set_ylabel(ylabel+' ('+yunit+')', fontsize=fontsettings[0])
    ax.set_xlabel(xlabel+' ('+xunit+')', fontsize=fontsettings[0])
    ax.set_xlim(xstart, xend)
    ax.set_ylim(ystart, yend)

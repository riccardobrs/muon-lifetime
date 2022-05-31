import matplotlib.pyplot as plt
from math import *
import numpy as np
from pathlib import Path
import os
import io
import glob
import pickle as pkl


def file_len(fname):
    with open(fname) as f:
        for j, l in enumerate(f):
            pass
    return j + 1


def DictFromArrayEfficiency(WorkDir, DetName):
    X1, Y1 = [], []
    X2, Y2 = [], []
    X3, Y3 = [], []
    Err1, Err2, Err3 = [], [], []

    paths = glob.glob(os.path.join(WorkDir, DetName + "*.txt"))
    paths.sort()
    i = 0
    for path in paths:
        with io.open(path, mode="r", encoding="utf-8") as fd:
            for line in fd:
                if i == 0:
                    values = [float(s) for s in line.split()]
                    X1.append(values[0])
                    eff1 = values[2] / values[3]
                    Y1.append(eff1)
                    Th1 = values[1]
                    Err1.append(sqrt(eff1 * (1 - eff1) / values[3]))
                elif i == 1:
                    values = [float(s) for s in line.split()]
                    X2.append(values[0])
                    eff2 = values[2] / values[3]
                    Y2.append(eff2)
                    Th2 = values[1]
                    Err2.append(sqrt(eff2 * (1 - eff2) / values[3]))
                elif i == 2:
                    values = [float(s) for s in line.split()]
                    X3.append(values[0])
                    eff3 = values[2] / values[3]
                    Y3.append(eff3)
                    Th3 = values[1]
                    Err3.append(sqrt(eff3 * (1 - eff3) / values[3]))
        i += 1
    DictTh1 = {'v': X1,
               'y': Y1,
               'th': Th1,
               'err': Err1}
    DictTh2 = {'v': X2,
               'y': Y2,
               'th': Th2,
               'err': Err2}
    DictTh3 = {'v': X3,
               'y': Y3,
               'th': Th3,
               'err': Err3}

    FinalDict = {'1': DictTh1,
                 '2': DictTh2,
                 '3': DictTh3}

    return FinalDict

def DictFromArrayThreshold(WorkDir, DetName):
    X1, Y1 = [], []
    X2, Y2 = [], []
    X3, Y3 = [], []
    X4, Y4 = [], []
    X5, Y5 = [], []
    X6, Y6 = [], []
    X7, Y7 = [], []
    X0, Y0 = [], []
    paths = glob.glob(os.path.join(WorkDir, DetName + "*.txt"))
    paths.sort()
    #xDict = {}
    #yDict = {}
    i = 0
    #j = 1
    for path in paths:
        with io.open(path, mode="r", encoding="utf-8") as fd:
            for line in fd:
                if i == 0:
                    values = [float(s) for s in line.split()]
                    X0.append(values[0])
                    rate0 = values[2] / values[1]
                    Y0.append(rate0)

                #xDict['X{0}.{1}'.format(i, j)] = values[0]
                #yDict['Y{0}.{1}'.format(i, j)] = values[2] / values[1]

                elif i == 1:
                    values = [float(s) for s in line.split()]
                    X1.append(values[0])
                    rate1 = values[2] / values[1]
                    Y1.append(rate1)
                elif i == 2:
                    values = [float(s) for s in line.split()]
                    X2.append(values[0])
                    rate2 = values[2] / values[1]
                    Y2.append(rate2)
                elif i == 3:
                    values = [float(s) for s in line.split()]
                    X3.append(values[0])
                    rate3 = values[2] / values[1]
                    Y3.append(rate3)
                elif i == 4:
                    values = [float(s) for s in line.split()]
                    X4.append(values[0])
                    rate4 = values[2] / values[1]
                    Y4.append(rate4)
                elif i == 5:
                    values = [float(s) for s in line.split()]
                    X5.append(values[0])
                    rate5 = values[2] / values[1]
                    Y5.append(rate5)
                elif i == 6:
                    values = [float(s) for s in line.split()]
                    X6.append(values[0])
                    rate6 = values[2] / values[1]
                    Y6.append(rate6)
                elif i == 7:
                    values = [float(s) for s in line.split()]
                    X7.append(values[0])
                    rate7 = values[2] / values[1]
                    Y7.append(rate7)

            #j += 1
        i += 1

    Dict0 = {'v': X0,
               'y': Y0}
    Dict1 = {'v': X1,
               'y': Y1}
    Dict2 = {'v': X2,
               'y': Y2}
    Dict3 = {'v': X3,
             'y': Y3}
    Dict4 = {'v': X4,
             'y': Y4}
    Dict5 = {'v': X5,
             'y': Y5}
    Dict6 = {'v': X6,
             'y': Y6}
    Dict7 = {'v': X7,
             'y': Y7}


    FinalDict = {'1': Dict0,
                 '2': Dict1,
                 '3': Dict2,
                 '4': Dict3,
                 '5': Dict4,
                 '6': Dict5,
                 '7': Dict6,
                 '8': Dict7}

    return FinalDict


def mkSublots(D, ax):
    ax.errorbar(D['2']['v'], D['2']['y'], yerr = D['2']['err'], label=D['2']['th'], elinewidth = 2, linewidth = 0.5)
    ax.errorbar(D['1']['v'], D['1']['y'], yerr = D['1']['err'], label=D['1']['th'], elinewidth = 2, linewidth = 0.5)
    ax.errorbar(D['3']['v'], D['3']['y'], yerr = D['3']['err'], label=D['3']['th'], elinewidth = 2, linewidth = 0.5)

    return ax

def mkSublotsTest(D, ax):
    ax.plot(D['1']['v'], D['1']['y'], '-r.')
    ax.plot(D['2']['v'], D['2']['y'], '-b.')
    ax.plot(D['3']['v'], D['3']['y'], '-g.')
    ax.plot(D['4']['v'], D['4']['y'], '-c.')
    ax.plot(D['5']['v'], D['5']['y'], '-m.')
    ax.plot(D['6']['v'], D['6']['y'], '-y.')
    ax.plot(D['7']['v'], D['7']['y'], '-k.')
    ax.plot(D['8']['v'], D['8']['y'], '-.', color='0.7')

    return ax

if __name__ == '__main__':
    Minosse = DictFromArrayEfficiency('./Efficiency', 'Minosse')
    Cerbero = DictFromArrayEfficiency('./Efficiency', 'Cerbero')
    Caronte = DictFromArrayEfficiency('./Efficiency', 'Caronte')

    Minosse_th = DictFromArrayThreshold('./RateVsThreshold', 'Minosse')
    Cerbero_th = DictFromArrayThreshold('./RateVsThreshold', 'Cerbero')
    Caronte_th = DictFromArrayThreshold('./RateVsThreshold', 'Caronte')

    fig, ax = plt.subplots()
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    fig3, ax3 = plt.subplots()
    fig4, ax4 = plt.subplots()
    fig5, ax5 = plt.subplots()

    ax = mkSublots(Minosse, ax)
    ax1 = mkSublots(Cerbero, ax1)
    ax2 = mkSublots(Caronte, ax2)

    ax3 = mkSublotsTest(Minosse_th, ax3)
    ax4 = mkSublotsTest(Cerbero_th, ax4)
    ax5 = mkSublotsTest(Caronte_th, ax5)

    legend = ax.legend(loc='lower right', shadow=True, fontsize='medium')
    legend1 = ax1.legend(loc='lower right', shadow=True, fontsize='medium')
    legend2 = ax2.legend(loc='lower right', shadow=True, fontsize='medium')

    plt.title('Efficiency')
    plt.xlabel('Voltage (V)')
    plt.ylabel(r'Efficiency $\varepsilon$')

    pkl.dump(fig, open('./Pickle/Minosse_efficiency.pickle', 'wb'))
    pkl.dump(fig1, open('./Pickle/Caronte_efficiency.pickle', 'wb'))
    pkl.dump(fig2, open('./Pickle/Cerbero_efficiency.pickle', 'wb'))
    pkl.dump(fig3, open('./Pickle/Minosse_threshold.pickle', 'wb'))
    pkl.dump(fig4, open('./Pickle/Caronte_threshold.pickle', 'wb'))
    pkl.dump(fig5, open('./Pickle/Cerbero_threshold.pickle', 'wb'))

    plt.show()

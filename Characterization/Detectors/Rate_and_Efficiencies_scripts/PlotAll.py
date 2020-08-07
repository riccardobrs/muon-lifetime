import matplotlib.pyplot as plt
from math import *
import numpy as np
from pathlib import Path
import os
import io
import glob
import pickle as pkl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
from matplotlib import cm


# This function measures the lenght of a file
def file_len(fname):
    with open(fname) as f:
        for j, l in enumerate(f):
            pass
    return j + 1


# This function stores all the data of the files
def DictFromArrayEfficiency(WorkDir, DetName):
    paths = glob.glob(os.path.join(WorkDir, DetName + "*.txt"))  # It stores every file that match in a list
    l = len(paths)
    paths.sort()
    f_l = []
    xDict = {}
    yDict = {}
    err_yDict = {}
    i = 0
    j = 1
    for path in paths:
        with io.open(path, mode="r", encoding="utf-8") as fd:
            for line in fd:
                if not line.startswith('#'):
                    values = [float(s) for s in line.split()]
                    xDict['X{0}.{1}'.format(i, j)] = values[0]  # It's storing the x values in a dictionary
                    yDict['Y{0}.{1}'.format(i, j)] = values[2] / values[3]  # It's storing the y values in a dictionary
                    eff = values[2] / values[3]  # It's calculating the err_y and after it'll store in a dictionary
                    err_yDict['eY{0}.{1}'.format(i, j)] = sqrt(eff * (1 - eff) / values[3])
                    j += 1
        f_l.append(file_len(path) - 1)
        j = 0
        i += 1  # The dictionary is something like xDict = {x0.0 : ..., x0.1: ..., ..., xi.j: ...} (same for the others)

    x_tot = list(xDict.values())  # It transforms the dictionary in a list so it can split the list easily
    y_tot = list(yDict.values())
    err_y_tot = list(err_yDict.values())
    FinalDict_x, FinalDict_y, FinalDict_err_y = {}, {}, {}

    # In the next loop it cut every list after the corresponding length of file and stores every list obtained in a
    # dictionary
    # Ex: first file has 3 lines, the second 5.
    # x_tot = [f_file1, f_file2, f_file3, s_file1, s_file2, s_file3, s_file4, s_file5]
    # After this loop -> FinalDict_x = {'x0': [f_file1, f_file2, f_file3],
    #                                   'x1': [s_file1, s_file2, s_file3, s_file4, s_file5]}

    for k in range(l + 1):
        if 0 < k <= l:
            FinalDict_x['x{0}'.format(k)] = x_tot[sum(f_l[:k - 1]):sum(f_l[:k])]
            FinalDict_y['y{0}'.format(k)] = y_tot[sum(f_l[:k - 1]):sum(f_l[:k])]
            FinalDict_err_y['e_y{0}'.format(k)] = err_y_tot[sum(f_l[:k - 1]):sum(f_l[:k])]
    # It stores every dictionary in a final dictionary
    FD = {'0': FinalDict_x,
          '1': FinalDict_y,
          '2': FinalDict_err_y}
    return FD


# This fucntion is very similar to the previous
def DictFromArrayThreshold(WorkDir, DetName):
    paths = glob.glob(os.path.join(WorkDir, DetName + "*.txt"))
    l = len(paths)
    paths.sort()
    f_l = []
    xDict = {}
    yDict = {}
    err_yDict = {}
    i = 0
    j = 1
    for path in paths:
        with io.open(path, mode="r", encoding="utf-8") as fd:
            for line in fd:
                if not line.startswith('#'):
                    values = [float(s) for s in line.split()]
                    xDict['X{0}.{1}'.format(i, j)] = values[0]
                    yDict['Y{0}.{1}'.format(i, j)] = values[2] / values[1]
                    err_yDict['eX{0}.{1}'.format(i, j)] = sqrt(values[2]) / values[1]
                    j += 1
        f_l.append(file_len(path) - 1)
        i += 1

    x_tot = list(xDict.values())
    y_tot = list(yDict.values())
    err_y_tot = list(err_yDict.values())
    FinalDict_x, FinalDict_y, FinalDict_err_y = {}, {}, {}

    for k in range(l + 1):
        if 0 < k <= l:
            FinalDict_x['x{0}'.format(k)] = x_tot[sum(f_l[:k - 1]):sum(f_l[:k])]
            FinalDict_y['y{0}'.format(k)] = y_tot[sum(f_l[:k - 1]):sum(f_l[:k])]
            FinalDict_err_y['e_y{0}'.format(k)] = err_y_tot[sum(f_l[:k - 1]):sum(f_l[:k])]
    FD = {'0': FinalDict_x,
          '1': FinalDict_y,
          '2': FinalDict_err_y}
    return FD


# This fucntion is very similar to the previous
def DictFromArrayVoltage(WorkDir, DetName):
    paths = glob.glob(os.path.join(WorkDir, DetName + "*.txt"))
    if DetName == 'Cerbero':
        paths.remove(os.path.join(WorkDir, "Cerbero_40mV.txt"))
    l = len(paths)
    paths.sort()
    f_l = []
    xDict = {}
    yDict = {}
    err_yDict = {}
    i = 0
    j = 1
    for path in paths:
        with io.open(path, mode="r", encoding="utf-8") as fd:
            for line in fd:
                if not line.startswith('#'):
                    values = [float(s) for s in line.split()]
                    xDict['X{0}.{1}'.format(i, j)] = values[0]
                    yDict['Y{0}.{1}'.format(i, j)] = values[2] / values[1]
                    err_yDict['eX{0}.{1}'.format(i, j)] = sqrt(values[2]) / values[1]
                    j += 1
        f_l.append(file_len(path) - 1)
        i += 1

    x_tot = list(xDict.values())
    y_tot = list(yDict.values())
    err_y_tot = list(err_yDict.values())
    FinalDict_x, FinalDict_y, FinalDict_err_y = {}, {}, {}

    for k in range(l + 1):
        if 0 < k <= l:
            FinalDict_x['x{0}'.format(k)] = x_tot[sum(f_l[:k - 1]):sum(f_l[:k])]
            FinalDict_y['y{0}'.format(k)] = y_tot[sum(f_l[:k - 1]):sum(f_l[:k])]
            FinalDict_err_y['e_y{0}'.format(k)] = err_y_tot[sum(f_l[:k - 1]):sum(f_l[:k])]

    FD = {'0': FinalDict_x,
          '1': FinalDict_y,
          '2': FinalDict_err_y}
    return FD


# In this function the program creates the subplots
def mkSublots(WorkDir, DetName, D, ax):
    mV = glob.glob(os.path.join(WorkDir, DetName + "*.txt"))  # It stores every file that match in a list
    mk_l = len(mV)
    if DetName == 'Cerbero' and WorkDir != './Characterization/Detectors/Efficiency':
        mk_l = mk_l - 1
    mV.sort()
    To_Remove = [os.path.join(WorkDir, DetName), '_', '.txt']  # It creates a list with every word to replace
    # In this loop the program replace every word that is not necessary, because in this way we can obtain the
    # name to put in the legend
    for t in To_Remove:
        for i in range(len(mV)):
            mV[i] = mV[i].replace(t, '')
            if mV[i].startswith('0'):
                mV[i] = mV[i][1:]
    # In this loop it fill the errorbar.
    for k in range(mk_l):
        # check if x are correctly sorted
        if not D['0']['x{0}'.format(k + 1)] == sorted(D['0']['x{0}'.format(k + 1)]):
            sorted_xye = []
            sorting_counter = 0
            for ns_x in D['0']['x{0}'.format(k + 1)]:
                couple_xye = []
                couple_xye.append(ns_x)
                couple_xye.append(D['1']['y{0}'.format(k + 1)][sorting_counter])
                couple_xye.append(D['2']['e_y{0}'.format(k + 1)][sorting_counter])
                sorted_xye.append(couple_xye)
                sorting_counter = sorting_counter + 1
            sorted_xye = sorted(sorted_xye, key=lambda k: k[0])  # list of couples [x,y,err] is sorted on the x value
            sorting_counter = 0
            for s_x in sorted_xye:
                D['0']['x{0}'.format(k + 1)][sorting_counter] = s_x[0]
                D['1']['y{0}'.format(k + 1)][sorting_counter] = s_x[1]
                D['2']['e_y{0}'.format(k + 1)][sorting_counter] = s_x[2]
                sorting_counter = sorting_counter + 1
            print('(x,y,err) with index {0} have been correctly sorted on x'.format(k))
        ax.errorbar(D['0']['x{0}'.format(k + 1)], D['1']['y{0}'.format(k + 1)], yerr=D['2']['e_y{0}'.format(k + 1)],
                    label=mV[k], elinewidth=2, linewidth=0.8)
        ax.grid(True, linestyle='--')
        ax.set_title(WorkDir.replace('./Characterization/Detectors/', '') + ' of ' + DetName, color='black')
        ax.set_facecolor('white')
        # labelcolor='tab:orange'
        ax.tick_params(labelcolor='black')

        # color='peachpuff'

        if WorkDir == './Characterization/Detectors/Efficiency':
            ax.set_xlabel('Voltage (V)', color='black')
            ax.set_ylabel(r'Efficiency $\varepsilon$', color='black')
        elif WorkDir.replace('./Characterization/Detectors/', '').replace('RateVs', '') == 'Threshold':
            ax.set_xlabel(WorkDir.replace('./Characterization/Detectors/', '').replace('RateVs', '') + ' (mV)', color='black')
            ax.set_ylabel('Rate (Hz)', color='black')
        elif WorkDir.replace('./Characterization/Detectors/', '').replace('RateVs', '') == 'Voltage':
            ax.set_xlabel(WorkDir.replace('./Characterization/Detectors/', '').replace('RateVs', '') + ' (V)', color='black')
            ax.set_ylabel('Rate (Hz)', color='black')
    return ax


def main():
    Minosse = DictFromArrayEfficiency('./Characterization/Detectors/Efficiency', 'Minosse')
    Cerbero = DictFromArrayEfficiency('./Characterization/Detectors/Efficiency', 'Cerbero')
    Caronte = DictFromArrayEfficiency('./Characterization/Detectors/Efficiency', 'Caronte')

    Minosse_th = DictFromArrayThreshold('./Characterization/Detectors/RateVsThreshold', 'Minosse')
    Cerbero_th = DictFromArrayThreshold('./Characterization/Detectors/RateVsThreshold', 'Cerbero')
    Caronte_th = DictFromArrayThreshold('./Characterization/Detectors/RateVsThreshold', 'Caronte')

    Minosse_V = DictFromArrayVoltage('./Characterization/Detectors/RateVsVoltage', 'Minosse')
    Caronte_V = DictFromArrayVoltage('./Characterization/Detectors/RateVsVoltage', 'Caronte')
    Cerbero_V = DictFromArrayVoltage('./Characterization/Detectors/RateVsVoltage', 'Cerbero')

    # facecolor=(.18, .31, .31)
    fig, ax = plt.subplots()
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    fig3, ax3 = plt.subplots()
    fig4, ax4 = plt.subplots()
    fig5, ax5 = plt.subplots()

    fig6, ax6 = plt.subplots()
    fig7, ax7 = plt.subplots()
    fig8, ax8 = plt.subplots()

    ax = mkSublots('./Characterization/Detectors/Efficiency', 'Minosse', Minosse, ax)
    ax1 = mkSublots('./Characterization/Detectors/Efficiency', 'Cerbero', Cerbero, ax1)
    ax2 = mkSublots('./Characterization/Detectors/Efficiency', 'Caronte', Caronte, ax2)

    ax3 = mkSublots('./Characterization/Detectors/RateVsThreshold', 'Minosse', Minosse_th, ax3)
    ax4 = mkSublots('./Characterization/Detectors/RateVsThreshold', 'Cerbero', Cerbero_th, ax4)
    ax5 = mkSublots('./Characterization/Detectors/RateVsThreshold', 'Caronte', Caronte_th, ax5)

    ax6 = mkSublots('./Characterization/Detectors/RateVsVoltage', 'Minosse', Minosse_V, ax6)
    ax7 = mkSublots('./Characterization/Detectors/RateVsVoltage', 'Caronte', Caronte_V, ax7)
    ax8 = mkSublots('./Characterization/Detectors/RateVsVoltage', 'Cerbero', Cerbero_V, ax8)

    legend = ax.legend(loc='best', shadow=True, fontsize='medium')
    legend1 = ax1.legend(loc='best', shadow=True, fontsize='medium')
    legend2 = ax2.legend(loc='best', shadow=True, fontsize='medium')

    legend3 = ax3.legend(loc='best', shadow=True, fontsize='medium')
    legend4 = ax4.legend(loc='best', shadow=True, fontsize='medium')
    legend5 = ax5.legend(loc='best', shadow=True, fontsize='medium')

    legend6 = ax6.legend(loc='best', shadow=True, fontsize='medium', ncol=2)
    legend7 = ax7.legend(loc='best', shadow=True, fontsize='medium', ncol=2)
    legend8 = ax8.legend(loc='best', shadow=True, fontsize='medium', ncol=2)

    # These following commands are needed to save the graph in the .pickle format
    pkl.dump(fig, open('./Plots/Pickle/Minosse_efficiency.pickle', 'wb'))
    pkl.dump(fig1, open('./Plots/Pickle/Cerbero_efficiency.pickle', 'wb'))
    pkl.dump(fig2, open('./Plots/Pickle/Caronte_efficiency.pickle', 'wb'))
    pkl.dump(fig3, open('./Plots/Pickle/Minosse_threshold_single.pickle', 'wb'))
    pkl.dump(fig4, open('./Plots/Pickle/Cerbero_threshold_single.pickle', 'wb'))
    pkl.dump(fig5, open('./Plots/Pickle/Caronte_threshold_single.pickle', 'wb'))
    pkl.dump(fig6, open('./Plots/Pickle/Minosse_voltage_single.pickle', 'wb'))
    pkl.dump(fig7, open('./Plots/Pickle/Caronte_voltage_single.pickle', 'wb'))
    pkl.dump(fig8, open('./Plots/Pickle/Cerbero_voltage_single.pickle', 'wb'))

    """fig.savefig('./Plots/eff_minosse.png', dpi=fig.dpi)
    print('./Plots/eff_minosse.png correctly saved')
    fig1.savefig('./Plots/eff_cerbero.png', dpi=fig1.dpi)
    print('./Plots/eff_cerbero.png correctly saved')
    fig2.savefig('./Plots/eff_caronte.png', dpi=fig2.dpi)
    print('./Plots/eff_caronte.png correctly saved')
    fig3.savefig('./Plots/rate_threshold_minosse.png', dpi=fig3.dpi)
    print('./Plots/rate_threshold_minosse.png correctly saved')
    fig4.savefig('./Plots/rate_threshold_cerbero.png', dpi=fig4.dpi)
    print('./Plots/rate_threshold_cerbero.png correctly saved')
    fig5.savefig('./Plots/rate_threshold_caronte.png', dpi=fig5.dpi)
    print('./Plots/rate_threshold_caronte.png correctly saved')
    fig6.savefig('./Plots/rate_bias_minosse.png', dpi=fig6.dpi)
    print('./Plots/rate_bias_minosse.png correctly saved')
    fig7.savefig('./Plots/rate_bias_caronte.png', dpi=fig7.dpi)
    print('./Plots/rate_bias_caronte.png correctly saved')
    fig8.savefig('./Plots/rate_bias_cerbero.png', dpi=fig8.dpi)
    print('./Plots/rate_bias_cerbero.png correctly saved')"""

    plt.show()


if __name__ == '__main__':
    main()

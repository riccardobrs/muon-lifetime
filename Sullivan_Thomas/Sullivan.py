import configparser
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.gridspec as gridspec
from math import *
from numpy import *
import numpy as np
from scipy.stats import norm
from pathlib import Path
import os
import io
import glob
import pickle as pkl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
from matplotlib import cm


def sullivan(a_1, b_1, a_2, b_2, l):
    alfa = 0.5 * (a_1 + a_2)
    beta = 0.5 * (b_1 + b_2)
    gamma = 0.5 * (a_1 - a_2)
    delta = 0.5 * (b_1 - b_2)

    a2 = alfa ** 2
    b2 = beta ** 2
    c2 = gamma ** 2
    d2 = delta ** 2
    l2 = l ** 2

    num_1 = l2 + a2 + d2
    num_2 = l2 + c2 + b2
    den_1 = l2 + a2 + b2
    den_2 = l2 + c2 + d2

    s1 = l2 * log((num_1 / den_1) * (num_2 / den_2))
    s2 = 2 * alfa * sqrt(l2 + b2) * atan(alfa / sqrt(l2 + a2))
    s3 = 2 * beta * sqrt(l2 + a2) * atan(beta / sqrt(l2 + b2))
    s4 = 2 * alfa * sqrt(l2 + d2) * atan(alfa / sqrt(l2 + d2))
    s5 = 2 * beta * sqrt(l2 + c2) * atan(beta / sqrt(l2 + c2))
    s6 = 2 * gamma * sqrt(l2 + b2) * atan(gamma / sqrt(l2 + b2))
    s7 = 2 * delta * sqrt(l2 + a2) * atan(delta / sqrt(l2 + a2))
    s8 = 2 * gamma * sqrt(l2 + d2) * atan(gamma / sqrt(l2 + d2))
    s9 = 2 * delta * sqrt(l2 + c2) * atan(delta / sqrt(l2 + c2))

    G = s1 + s2 + s3 - s4 - s5 - s6 - s7 + s8 + s9

    return G


def loading_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    values = {'a1': float(config['Data']['a1']),
              'b1': float(config['Data']['b1']),
              'a2': float(config['Data']['a2']),
              'b2': float(config['Data']['b2']),
              'l': float(config['Data']['l'])}

    return values


def rate_calculator(WorkDir, DetName):
    paths = glob.glob(os.path.join(WorkDir, DetName + "*.txt"))  # It stores every file that match in a list
    paths.sort()
    doppie = np.array([])
    for path in paths:
        with io.open(path, mode="r", encoding="utf-8") as fd:
            for line in fd:
                if not line.startswith('#'):
                    values = [float(s) for s in line.split()]
                    doppie = np.append(doppie, values[3] / 180)
    return doppie


if __name__ == '__main__':
    v = loading_config('configSullivan.txt')
    G = sullivan(v['a1'], v['b1'], v['a2'], v['b2'], v['l'])

    # print('Geometrical Factor: ' + str(G))

    rate_m = rate_calculator('./Efficiency', 'Minosse')
    m_m, s_m = stats.norm.fit(rate_m)  # get mean and standard deviation
    """print('Minosse')
    print('Mean: ' + str(m_m))
    print('Std. Deviation: ' + str(s_m))"""

    rate_c = rate_calculator('./Efficiency', 'Caronte')
    m_c, s_c = stats.norm.fit(rate_c)  # get mean and standard deviation
    """print('Caronte')
    print('Mean: ' + str(m_c))
    print('Std. Deviation: ' + str(s_c))"""

    rate_ce = rate_calculator('./Efficiency', 'Cerbero')
    m_ce, s_ce = stats.norm.fit(rate_ce)  # get mean and standard deviation
    """print('Cerbero')
    print('Mean: ' + str(m_ce))
    print('Std. Deviation: ' + str(s_ce))"""

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot()
    x = np.arange(0.01, 1, 0.01)
    f2 = np.vectorize(sullivan)
    sul = ax.plot(x, f2(v['a1'], v['b1'], v['a2'], v['b2'], x), label='G', linestyle='-')
    ax.set_title('Geometrical factor')
    ax.set_xlabel('l $[m]$', color='black')
    ax.set_ylabel(r'G $[m^{2}\cdot sr]$', color='black')
    ax.vlines(x=v['l'], ymin=0, ymax=G, color='r')
    ax.hlines(y=G, xmin=0, xmax=v['l'], color='r')
    legend = ax.legend(loc='best', shadow=True, fontsize='medium')

    print("Intensita' [m^(-2)*s^(-1)*sr^(-1)]:\n"
          'G con Minosse/Caronte in mezzzo: ' + str(G) + '\n'
          'Minosse: ' + str(m_m / G) + '\n'
          'Caronte: ' + str(m_c / G) + '\n'
          'Cerbero: ' + str(m_ce / G),
          file=open("Sullivan_output.txt", "w"))
    # plt.show()

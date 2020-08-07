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


def rate(WorkDir1, WorkDir2, DetNameCentrale, DetNameUp, Threshold, Voltage):
    paths = glob.glob(os.path.join(WorkDir1, DetNameCentrale + "*.txt"))  # It stores every file that match in a list
    paths2 = glob.glob(os.path.join(WorkDir2, DetNameUp + "_{}mV.txt".format(Threshold)))
    doppie = np.array([])
    singole = np.array([])
    for path in paths:
        with io.open(path, mode="r", encoding="utf-8") as fd:
            for line in fd:
                if not line.startswith('#'):
                    values = [float(s) for s in line.split()]
                    doppie = np.append(doppie, values[3] / 180)
    for path in paths2:
        with io.open(path, mode="r", encoding="utf-8") as fd:
            for line in fd:
                if not line.startswith('#'):
                    values = [float(s) for s in line.split()]
                    if values[0] == Voltage:
                        singole = np.append(singole, values[2] / values[1])
    return [singole, doppie]


def loading_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    values = {'det_up': str(config['Data']['detector_up']),
              'det_down': str(config['Data']['detector_down']),
              'th': str(config['Data']['threshold_up']),
              'volt': float(config['Data']['voltage_up']),
              'G_mu_m': float(config['Data']['G_mu_minosse']),
              'G_mu_c': float(config['Data']['G_mu_caronte']),
              'G_mu_ce': float(config['Data']['G_mu_cerbero']),
              'G_g_m': float(config['Data']['G_g_minosse']),
              'G_g_c': float(config['Data']['G_g_caronte']),
              'G_g_ce': float(config['Data']['G_g_cerbero']),
              'G_mu_s': float(config['Data']['G_mu_s']),
              'G_g_s': float(config['Data']['G_g_s'])
              }

    return values


def background(rateSingole, rateDoppie, G_gamma_1, G_gamma_t, G_mu_1, G_mu_t, eff):
    x = (rateSingole * eff * G_gamma_t - rateDoppie * G_gamma_1) / (
            G_mu_1 - G_gamma_1 - rateSingole * eff * (G_mu_t - G_gamma_t))
    return x


if __name__ == '__main__':
    conf_file = loading_config('configBackground.txt')
    rates = rate('./Efficiency', './RateVsVoltage', 'Caronte',
                 'Cerbero', conf_file['th'], conf_file['volt'])
    mean_s = np.mean(rates[0])
    print(mean_s)
    mean_d = np.mean(rates[1])
    x = background(mean_s, mean_d, conf_file['G_g_s'], conf_file['G_g_c'], conf_file['G_mu_s'],
                   conf_file['G_mu_c'], 0.9948)
    print(x)

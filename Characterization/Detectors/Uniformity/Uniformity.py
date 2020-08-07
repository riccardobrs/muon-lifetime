import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.gridspec as gridspec
from math import *
from numpy import *
import numpy as np
from pathlib import Path
import os
import io
import glob
import pickle as pkl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
from matplotlib import cm


def mkUniformity(WorkDir, DetName, ax):
    path1 = glob.glob(os.path.join(WorkDir, DetName + "*.txt"))
    path1.sort()

    test = []
    for path in path1:
        z = np.array([])
        with io.open(path, mode="r", encoding="utf-8") as fd:
            for line in fd:
                if not line.startswith('#'):
                    values = [float(s) for s in line.split()]
                    z = np.append(z, (values[0] / values[1]))
        test.append(z)
    Z = np.array(test)
    half_Z = Z/2
    unif = half_Z.sum(axis=1)
    unif_1 = np.around(unif, decimals=2)
    unif_matrix = np.tile(unif_1, (3,1))

    im = ax.imshow(unif_matrix, cmap=cm.Blues, vmin=-10, vmax=10,aspect='auto')
    ax.set_title('Uniformity of ' + DetName)
    ax.axvline(x=0.5, color='k')
    ax.axvline(x=1.5, color='k')

    for j in range(3):
        text = ax.text(j, 1, unif_matrix[1, j],
                        ha="center", va="center", color='k')

    return ax, im


def mkFineUniformity(WorkDir, DetName, ax):
    path1 = glob.glob(os.path.join(WorkDir, DetName + "*.txt"))
    path1.sort()

    test = []
    for path in path1:
        z = np.array([])
        with io.open(path, mode="r", encoding="utf-8") as fd:
            for line in fd:
                if not line.startswith('#'):
                    values = [float(s) for s in line.split()]
                    z = np.append(z, (values[0] / values[1]))
        test.append(z)
    Z = np.array(test)
    unif = Z.transpose()
    unif_1 = np.around(unif, decimals=4)
    unif_matrix = np.tile(unif_1, (3,1))

    im = ax.imshow(unif_matrix, cmap=cm.Blues, aspect='auto')
    ax.set_title('Fine uniformity of ' + DetName)
    ax.axvline(x=0.5, color='k')
    ax.axvline(x=1.5, color='k')
    ax.axvline(x=2.5, color='k')
    ax.axvline(x=3.5, color='k')
    ax.axvline(x=4.5, color='k')
    ax.axvline(x=5.5, color='k')
    ax.axvline(x=6.5, color='k')
    ax.axvline(x=7.5, color='k')

    for j in range(9):
        text = ax.text(j, 1, unif_matrix[1, j],
                        ha="center", va="center", color='k')

    return ax, im


def main():
    fig = plt.figure(figsize=(10, 5))
    fig1 = plt.figure(figsize=(10, 5))
    fig2 = plt.figure(figsize=(10, 5))
    fig3 = plt.figure(figsize=(10, 5))

    ax1 = fig.add_subplot()
    ax1, im1 = mkUniformity('./Uniformity', 'Minosse', ax1)
    ax1.axes.get_xaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)

    ax2 = fig1.add_subplot()
    ax2, im2 = mkUniformity('./Uniformity', 'Caronte', ax2)
    ax2.axes.get_xaxis().set_visible(False)
    ax2.axes.get_yaxis().set_visible(False)

    ax3 = fig2.add_subplot()
    ax3, im3 = mkUniformity('./Uniformity', 'Cerbero', ax3)
    ax3.axes.get_xaxis().set_visible(False)
    ax3.axes.get_yaxis().set_visible(False)

    ax4 = fig3.add_subplot()
    ax4, im4 = mkFineUniformity('./Uniformity/Fine', 'Minosse', ax4)
    ax4.axes.get_xaxis().set_visible(False)
    ax4.axes.get_yaxis().set_visible(False)
    cbar = fig3.colorbar(im4)
    cbar.set_label('Efficiency', rotation=270, labelpad=15)

    pkl.dump(fig, open('./Plots/Pickle/Minosse_uniformity.pickle', 'wb'))
    pkl.dump(fig1, open('./Plots/Pickle/Caronte_uniformity.pickle', 'wb'))
    pkl.dump(fig2, open('./Plots/Pickle/Cerbero_uniformity.pickle', 'wb'))
    pkl.dump(fig3, open('./Plots/Pickle/Minosse_fine_uniformity.pickle', 'wb'))

    plt.show()
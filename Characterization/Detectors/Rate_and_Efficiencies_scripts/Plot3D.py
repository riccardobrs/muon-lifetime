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


def plot3D(WorkDir1, WorkDir2, DetName):
    path1 = glob.glob(os.path.join(WorkDir1, DetName + "*.txt"))
    path2 = glob.glob(os.path.join(WorkDir2, DetName + "*.txt"))
    path3 = glob.glob(os.path.join(WorkDir1, DetName + "*.txt"))
    path4 = glob.glob(os.path.join(WorkDir2, DetName + "*.txt"))
    To_Remove1 = [os.path.join(WorkDir1, DetName), '_', 'm', 'V.txt']
    To_Remove2 = [os.path.join(WorkDir2, DetName), '_', 'm', 'V.txt']
    rate_dict = {}
    path1.sort()
    path2.sort()
    path3.sort()
    path4.sort()

    if DetName == 'Cerbero':
        path2.remove(os.path.join(WorkDir2, "Cerbero_40mV.txt"))
        path4.remove(os.path.join(WorkDir2, "Cerbero_40mV.txt"))

    for t in To_Remove1:
        for i in range(len(path1)):
            path1[i] = path1[i].replace(t, '')
    for t in To_Remove2:
        for j in range(len(path2)):
            path2[j] = path2[j].replace(t, '')
    z1 = []
    test = []
    for path in path4:
        z = np.array([])
        with io.open(path, mode="r", encoding="utf-8") as fd:
            for line in fd:
                if not line.startswith('#'):
                    values = [float(s) for s in line.split()]
                    z = np.append(z, (values[2] / values[1]))
                    z1.append(values[2] / values[1])
        test.append(z)
    Z = np.array(test)
    path1 = [int(i) for i in path1]
    path2 = [int(i) for i in path2]
    x = np.array(path1)
    y = np.array(path2)
    dz_ = np.array(z1)
    x_len = x.shape[0]
    y_len = y.shape[0]
    x_ = np.tile(x, y_len)
    y_ = np.repeat(y, x_len)
    z_ = np.zeros(x_len * y_len)
    dx_ = np.arange(x_len * y_len)
    dy_ = np.arange(x_len * y_len)
    dx_.fill(50)
    dy_.fill(10)

    final_dict = {'v': x_,
                  'y': y_,
                  'z': z_,
                  'dx': dx_,
                  'dy': dy_,
                  'dz': dz_,
                  'Z': Z,
                  'detector': DetName,
                  'x_label': x,
                  'y_label': y}

    return final_dict


def mkPlot3D(d, ax, ax1):
    dz_normed = d['dz'] / d['dz'].max()
    normed_cbar = colors.Normalize(dz_normed.min(), dz_normed.max())
    color = cm.jet(normed_cbar(dz_normed))

    ax.bar3d(d['v'], d['y'], d['z'], d['dx'], d['dy'], d['dz'], shade=True, color=color)
    # ax.set_title('3D Plot')
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('Threshold (mV)')
    ax.set_zlabel('Rate (Hz)', rotation=270)
    ax.view_init(ax.elev - 14, ax.azim + 220)

    im = ax1.imshow(d['Z'], cmap=plt.get_cmap('jet'), aspect='auto')
    ax1.set_xticks(np.arange(len(d['x_label'])))
    ax1.set_yticks(np.arange(len(d['y_label'])))
    ax1.set_xticklabels(d['x_label'])
    ax1.set_yticklabels(d['y_label'])

    # ax1.set_title('Heatmap')
    ax1.set_xlabel('Voltage (V)')
    ax1.set_ylabel('Threshold (mV)')

    return ax, im


def main():
    Caronte_values = plot3D('./Characterization/Detectors/RateVsThreshold',
                            './Characterization/Detectors/RateVsVoltage', 'Caronte')
    Minosse_values = plot3D('./Characterization/Detectors/RateVsThreshold',
                            './Characterization/Detectors/RateVsVoltage', 'Minosse')
    Cerbero_values = plot3D('./Characterization/Detectors/RateVsThreshold',
                            './Characterization/Detectors/RateVsVoltage', 'Cerbero')

    fig = plt.figure(figsize=(10, 5))
    fig1 = plt.figure(figsize=(10, 5))
    fig2 = plt.figure(figsize=(10, 5))

    spec = gridspec.GridSpec(ncols=2, nrows=1, figure=fig)
    spec1 = gridspec.GridSpec(ncols=2, nrows=1, figure=fig1)
    spec2 = gridspec.GridSpec(ncols=2, nrows=1, figure=fig2)

    ax = fig.add_subplot(spec[0, 0], projection='3d')
    ax1 = fig.add_subplot(spec[0, 1])
    ax, im = mkPlot3D(Caronte_values, ax, ax1)

    ax2 = fig1.add_subplot(spec1[0, 0], projection='3d')
    ax3 = fig1.add_subplot(spec1[0, 1])
    ax2, im1 = mkPlot3D(Minosse_values, ax2, ax3)

    ax4 = fig2.add_subplot(spec2[0, 0], projection='3d')
    ax5 = fig2.add_subplot(spec2[0, 1])
    ax4, im2 = mkPlot3D(Cerbero_values, ax4, ax5)

    cbar = fig.colorbar(im)
    cbar.set_label('Rate (Hz)', rotation=270, labelpad=15)
    cbar1 = fig1.colorbar(im1)
    cbar1.set_label('Rate (Hz)', rotation=270, labelpad=15)
    cbar2 = fig2.colorbar(im2)
    cbar2.set_label('Rate (Hz)', rotation=270, labelpad=15)

    fig.suptitle(Caronte_values['detector'], fontsize=16)
    fig1.suptitle(Minosse_values['detector'], fontsize=16)
    fig2.suptitle(Cerbero_values['detector'], fontsize=16)

    fig.subplots_adjust(left=0., right=0.95, wspace=0.34)
    fig1.subplots_adjust(left=0, right=0.95, wspace=0.34)
    fig2.subplots_adjust(left=0, right=0.95, wspace=0.34)

    pkl.dump(fig, open('./Plots/Pickle/Caronte_3D.pickle', 'wb'))
    pkl.dump(fig1, open('./Plots/Pickle/Minosse_3D.pickle', 'wb'))
    pkl.dump(fig2, open('./Plots/Pickle/Cerbero_3D.pickle', 'wb'))

    """fig.savefig('./Plot3D/3d_{0}.png'.format(Caronte_values['detector'].lower()), dpi=fig.dpi)
    print('./Plot3D/3d_{0}.png correctly saved'.format(Caronte_values['detector'].lower()))
    fig1.savefig('./Plot3D/3d_{0}.png'.format(Minosse_values['detector'].lower()), dpi=fig1.dpi)
    print('./Plot3D/3d_{0}.png correctly saved'.format(Minosse_values['detector'].lower()))
    fig2.savefig('./Plot3D/3d_{0}.png'.format(Cerbero_values['detector'].lower()), dpi=fig2.dpi)
    print('./Plot3D/3d_{0}.png correctly saved'.format(Cerbero_values['detector'].lower()))"""

    plt.show()


if __name__ == '__main__':
    main()

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
import io
import glob
import pickle as pkl
import sys
import argparse


def openPickle(opt):
    WorkDir = './Plots/Pickle'
    if opt == 1:
        paths = glob.glob(os.path.join(WorkDir, '*single.pickle'))
    elif opt == 2:
        paths = glob.glob(os.path.join(WorkDir, '*3D.pickle'))
    elif opt == 3:
        paths = glob.glob(os.path.join(WorkDir, '*efficiency.pickle'))
    elif opt == 4:
        paths = glob.glob(os.path.join(WorkDir, '*uniformity.pickle'))
    elif opt == 5:
        paths = glob.glob(os.path.join(WorkDir, 'Minosse*.pickle'))
    elif opt == 6:
        paths = glob.glob(os.path.join(WorkDir, 'Caronte*.pickle'))
    elif opt == 7:
        paths = glob.glob(os.path.join(WorkDir, 'Cerbero*.pickle'))
    elif opt == 8:
        paths = glob.glob(os.path.join(WorkDir, '*.pickle'))

    figDict = {}
    i = 0
    for path in paths:
        figDict['fig{0}'.format(path)] = pkl.load(open(paths[i], 'rb'))
        i += 1
    plt.show()


"""if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='plot the .pickle files with different options')
    parser.add_argument('-e', '--efficiency', action='store_true', help='Open only plot of efficiencies')
    parser.add_argument('-s', '--single', action='store_true', help='Open only plot of single rate')
    parser.add_argument('-a', '--all', action='store_true', help='Plot every .pickle files')
    parser.add_argument('-m', '--minosse', action='store_true', help='Plot every Minosse .pickle files')
    parser.add_argument('-c', '--caronte', action='store_true', help='Plot every Caronte .pickle files')
    parser.add_argument('-ce', '--cerbero', action='store_true', help='Plot every Cerbero .pickle files')
    parser.add_argument('-t', '--threeDim', action='store_true', help='Plot every 3D .pickle files')
    parser.add_argument('-u', '--uniformity', action='store_true', help='Plot every uniformity')
    args = parser.parse_args()

    WorkDir = './Pickle'

    if args.efficiency:
        print('Plot of efficiencies')
        paths = glob.glob(os.path.join(WorkDir, '*efficiency.pickle'))
    elif args.single:
        print('Plot of single rate')
        paths = glob.glob(os.path.join(WorkDir, '*single.pickle'))
    elif args.all:
        print('Plot everything')
        paths = glob.glob(os.path.join(WorkDir, '*.pickle'))
    elif args.minosse:
        print('Plot everything about Minosse')
        paths = glob.glob(os.path.join(WorkDir, 'Minosse*.pickle'))
    elif args.caronte:
        print('Plot everything about Caronte')
        paths = glob.glob(os.path.join(WorkDir, 'Caronte*.pickle'))
    elif args.cerbero:
        print('Plot everything about Cerbero')
        paths = glob.glob(os.path.join(WorkDir, 'Cerbero*.pickle'))
    elif args.threeDim:
        print('Plot every 3D graph')
        paths = glob.glob(os.path.join(WorkDir, '*3D.pickle'))
    elif args.uniformity:
        print('Plot every graph of uniformity')
        paths = glob.glob(os.path.join(WorkDir, '*uniformity.pickle'))

    figDict = {}
    i = 0
    for path in paths:
        figDict['fig{0}'.format(path)] = pkl.load(open(paths[i], 'rb'))
        i += 1
    plt.show()"""

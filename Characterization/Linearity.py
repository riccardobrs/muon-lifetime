from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from numpy import *
import numpy as np
import os
import glob
from scipy.stats import chisquare


def pars(workDir, freq):
    result = {}

    paths = glob.glob(os.path.join(workDir, freq + "*.xml"))
    for path, i in zip(paths, range(len(paths))):
        file_name = str(freq + '_{}'.format(i + 1))
        result[file_name] = {}
        infile = open(path, "r")
        contents = infile.read()
        soup = BeautifulSoup(contents, 'lxml')
        for event in soup.find_all('event'):
            for trace in event.find_all('trace'):
                result[file_name][event.attrs['id']] = [float(s) for s in trace.contents[0].split()]
    return result


def mkPlot(filename):
    xml = pars('./Characterization/Digitizer', filename)
    freq = np.array([])
    final_mean = np.array([])
    final_std = np.array([])

    for i in range(len(xml)):
        mean_freq = np.array([])
        std_freq = np.array([])
        for j in range(len(xml[filename + '_{}'.format(i + 1)].keys())):
            y = np.array(xml[filename + '_{}'.format(i + 1)]['{}'.format(j + 1)])
            y_d = np.diff(y)
            max_index = []
            min_index = []
            for e in y_d:
                max = np.argmax(y_d)
                min = np.argmin(y_d)
                if y_d[max] > 200:
                    max_index.append(max)
                    for k in range(-5, 5):
                        if 0 <= max + k <= len(y_d) - 1:
                            y_d[max + k] = 0
                elif y_d[min] < -200:
                    min_index.append(min)
                    for k in range(-5, 5):
                        if 0 <= min + k <= len(y_d) - 1:
                            y_d[min + k] = 0
                else:
                    break
            max_index.sort()
            min_index.sort()
            for t in range(len(min_index) - 1):
                freq = np.append(freq, 1 / ((min_index[t + 1] - min_index[t]) / (250 * (10 ** 6))))
            mean_freq = np.append(mean_freq, freq.mean())
            std_freq = np.append(std_freq, freq.std())

        final_mean = np.append(final_mean, mean_freq.mean())
        final_std = np.append(final_std, std_freq.mean())
    results = {'Frequenza': final_mean.mean() / (10 ** 6),
               'Std': final_std.mean() / (10 ** 6),
               'hist': freq / (10 ** 6)}
    return results


def main():
    n_bins = 20

    a = mkPlot('1MHz')
    b = mkPlot('3MHz')
    c = mkPlot('5MHz')
    d = mkPlot('10MHz')
    e = mkPlot('12MHz')
    f = mkPlot('450kHz')
    g = mkPlot('500kHz')
    h = mkPlot('700kHz')
    i = mkPlot('800kHz')
    l = mkPlot('990kHz')

    y = np.array(
        [f['Frequenza'], g['Frequenza'], h['Frequenza'], i['Frequenza'], l['Frequenza'], a['Frequenza'], b['Frequenza'],
         c['Frequenza'], d['Frequenza'], e['Frequenza']])
    y_err = np.array([f['Std'], g['Std'], h['Std'], i['Std'], l['Std'], a['Std'], b['Std'],
                      c['Std'], d['Std'], e['Std']])
    x = np.array([0.45, 0.5, 0.7, 0.8, 0.99, 1, 3, 5, 10, 12])

    data_hist = np.array(
        [f['hist'], g['hist'], h['hist'], i['hist'], l['hist'], a['hist'], b['hist'], c['hist'], d['hist'],
         e['hist']])

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot()

    fig1 = plt.figure(figsize=(10, 5))
    spec = gridspec.GridSpec(ncols=5, nrows=2, figure=fig1)
    ax1 = fig1.add_subplot(spec[0, 0])
    ax2 = fig1.add_subplot(spec[0, 1])
    ax3 = fig1.add_subplot(spec[0, 2])
    ax4 = fig1.add_subplot(spec[0, 3])
    ax5 = fig1.add_subplot(spec[0, 4])
    ax6 = fig1.add_subplot(spec[1, 0])
    ax7 = fig1.add_subplot(spec[1, 1])
    ax8 = fig1.add_subplot(spec[1, 2])
    ax9 = fig1.add_subplot(spec[1, 3])
    ax10 = fig1.add_subplot(spec[1, 4])

    h1 = ax1.hist(f['hist'], bins=n_bins)
    ax1.set_title('450kHz')

    h2 = ax2.hist(g['hist'], bins=n_bins)
    ax2.set_title('500kHz')

    h3 = ax3.hist(h['hist'], bins=n_bins)
    ax3.set_title('700kHz')

    h4 = ax4.hist(i['hist'], bins=n_bins)
    ax4.set_title('800kHz')

    h5 = ax5.hist(l['hist'], bins=n_bins)
    ax5.set_title('990kHz')

    h6 = ax6.hist(a['hist'], bins=n_bins)
    ax6.set_title('1MHz')

    h7 = ax7.hist(b['hist'], bins=n_bins)
    ax7.set_title('3MHz')

    h8 = ax8.hist(c['hist'], bins=n_bins)
    ax8.set_title('5MHz')

    h9 = ax9.hist(d['hist'], bins=n_bins)
    ax9.set_title('10MHz')

    h10 = ax10.hist(e['hist'], bins=n_bins)
    ax10.set_title('12MHz')

    linearity_plot = ax.errorbar(x, y, yerr=y_err * 10,
                                 label='Linearity data', ls='none', ecolor='r')
    coef = np.polyfit(x, y, 1)
    poly1d_fn = np.poly1d(coef)

    fit_label_1 = 'm = {}\n'.format(round(coef[0], 5))
    fit_label_2 = 'q = {}'.format(round(coef[1], 5))
    fit_label = fit_label_1 + fit_label_2

    fit_plot = ax.plot(x, poly1d_fn(x), '--k', linewidth=0.5, label=fit_label)
    legend = ax.legend(loc='upper left', shadow=True, fontsize='medium', prop={"size": 15})

    ax.set_xlabel('Nominal frequencies (MHz)', color='black', fontsize=15)
    ax.set_ylabel('Digitizer frequencies (MHz)', color='black', fontsize=15)

    """ax1.set_xlabel('', color='black')
    ax1.set_ylabel('Digitizer frequencies (MHz)', color='black')
    ax2.set_xlabel('Nominal frequencies (MHz)', color='black')
    ax2.set_ylabel('Digitizer frequencies (MHz)', color='black')
    ax3.set_xlabel('Nominal frequencies (MHz)', color='black')
    ax3.set_ylabel('Digitizer frequencies (MHz)', color='black')
    ax4.set_xlabel('Nominal frequencies (MHz)', color='black')
    ax4.set_ylabel('Digitizer frequencies (MHz)', color='black')
    ax5.set_xlabel('Nominal frequencies (MHz)', color='black')
    ax5.set_ylabel('Digitizer frequencies (MHz)', color='black')
    ax6.set_xlabel('Nominal frequencies (MHz)', color='black')
    ax6.set_ylabel('Digitizer frequencies (MHz)', color='black')
    ax7.set_xlabel('Nominal frequencies (MHz)', color='black')
    ax7.set_ylabel('Digitizer frequencies (MHz)', color='black')
    ax8.set_xlabel('Nominal frequencies (MHz)', color='black')
    ax8.set_ylabel('Digitizer frequencies (MHz)', color='black')
    ax9.set_xlabel('Nominal frequencies (MHz)', color='black')
    ax9.set_ylabel('Digitizer frequencies (MHz)', color='black')
    ax10.set_xlabel('Nominal frequencies (MHz)', color='black')
    ax10.set_ylabel('Digitizer frequencies (MHz)', color='black')"""

    print(' ----------------------- LEGEND AND UNITS ----------------------\n'
          '|                The frequencies are reported in [MHz]           |\n'
          ' ---------------------------------------------------------------\n\n'
          '                         *** RESULTS ***\n\n'
          'Nominal Frequencies | Derived Frequencies +/- Dev. Std                     \n'
          '---------------------------------------------------------------------------\n'
          '             450kHz | ' + str(f['Frequenza']) + ' +/- ' + str(f['Std']) + '\n'
          '             500kHz | ' + str(g['Frequenza']) + ' +/- ' + str(g['Std']) + '\n'
          '             700kHz | ' + str(h['Frequenza']) + ' +/- ' + str(h['Std']) + '\n'
          '             800kHz | ' + str(i['Frequenza']) + ' +/- ' + str(i['Std']) + '\n'
          '             990kHz | ' + str(l['Frequenza']) + ' +/- ' + str(l['Std']) + '\n'
          '               1MHz | ' + str(a['Frequenza']) + ' +/- ' + str(a['Std']) + '\n'
          '               3MHz | ' + str(b['Frequenza']) + ' +/- ' + str(b['Std']) + '\n'
          '               5MHz | ' + str(c['Frequenza']) + ' +/- ' + str(c['Std']) + '\n'
          '              10MHz | ' + str(d['Frequenza']) + ' +/- ' + str(d['Std']) + '\n'
          '              12MHz | ' + str(e['Frequenza']) + ' +/- ' + str(e['Std']) + '\n'
          '---------------------------------------------------------------------------\n\n'
          '                         *** FIT RESULTS ***\n\n'
          'Slope (m): ' + str(coef[0]) + '\n'
          'Intercept (q): ' + str(coef[1]) + '\n'
          'Chi-square: ' + str(chisquare(f_obs=y, f_exp=x)) + '\n'
          'Delta (%): ' + str(abs(1 - coef[0]) * 100),
          file=open("./Characterization/Linearity_output.txt", "w"))

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()

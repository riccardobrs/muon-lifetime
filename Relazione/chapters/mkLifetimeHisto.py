import argparse
import ROOT
import numpy as np

def N_pulses (array_y, threshold):
    
    N = 0
    i = 0
    pulse_end = []
    
    pulse = False
    
    for y in array_y:
        if y < threshold and not pulse: #negative pulses
            pulse = True
            N += 1
        if y > threshold and pulse:
            pulse = False
            pulse_end.append(i)
            
        i += 1
    
    return N, pulse_end

def events_partition (inputpath, rate):
    
    rejected = {}
    N_rejected = 0
    N_kept_up = 0
    N_kept_down = 0
    N = 1
    
    t_up = []
    t_down = []
    
    xml_to_root = ROOT.TFile (inputpath, 'READ')
    
    g0 = ROOT.TGraph()
    g1 = ROOT.TGraph()
    
    event_exists = ROOT.gDirectory.cd('Event{0}'.format(N))
    
    dx = 1./rate #differential for the derivative
    
    while(event_exists):
        
        ROOT.gDirectory.GetObject("channel0", g0)
        ROOT.gDirectory.GetObject("channel1", g1)
        g0_x = np.array(g0.GetX())
        g0_y = np.array(g0.GetY())
        g1_x = np.array(g1.GetX())
        g1_y = np.array(g1.GetY())
        
        pulses_0, pulses_end_0 = N_pulses(g0_y, args.threshold0)
        pulses_1, pulses_end_1  = N_pulses(g1_y, args.threshold1)
            
        if pulses_0 == 2 and pulses_1 == 0:
            N_kept_up += 1
            dy0 = np.diff(g0_y)/dx
            t = g0_x[list(dy0).index(min(dy0[pulses_end_0[0]:]))] - g0_x[list(dy0).index(min(dy0[:pulses_end_0[0]]))]
            t_up.append(t)
            
        elif pulses_0 == 1 and pulses_1 == 1:
            N_kept_down += 1
            dy0 = np.diff(g0_y)/dx
            dy1 = np.diff(g1_y)/dx
            t = g1_x[list(dy1).index(min(dy1))] - g0_x[list(dy0).index(min(dy0))]
            t_down.append(t)
            
        else:
            N_rejected += 1
            key = '{0}{1}'.format(pulses_0, pulses_1)
            if not key in rejected.keys():
                rejected[key] = 1
            else:
                rejected[key] += 1
        
        N += 1
        event_exists = ROOT.gDirectory.cd('../Event{0}'.format(N))
    
    
    print '\nUp decays:\t\t', N_kept_up
    print 'Down decays:\t\t', N_kept_down, '\n'
    print 'Events rejected:\t{0}/{1}'.format(N_rejected, N-1)
    for (key, val) in sorted(rejected.items(), key=lambda x: x[1], reverse=True):
        print '({0} up, {1} down):\t\t{2}'.format(key[0], key[1], val)
    
    xml_to_root.Close()
    
    return t_up, t_down
    
    
def makePlot (data, histo_name, NBin, xmin, xmax, fit_option, fit_min, fit_max, path):
    
    histo = ROOT.TH1D(histo_name, '', NBin, xmin, xmax)
    fit_f = ROOT.TF1('fit_f', '[0]*exp(-x/[1]) + [2]', xmin, xmax)
    
    histo.GetXaxis().SetTitle('#Deltat [#mus]')
    histo.GetYaxis().SetTitle('Counts')
    
    fit_f.SetParName(0, 'Amp')
    fit_f.SetParName(1, '#tau')
    fit_f.SetParName(2, 'B')
    fit_f.SetParameter(1, 2.12)
    
    for d in data:
        histo.Fill(d)
    
    out_file = ROOT.TFile('lifetime_{0}.root'.format(path), 'RECREATE')
    
    histo.Write('histogram')
    
    c = ROOT.TCanvas()
    c.cd()
    histo.Draw()
    histo.Fit('fit_f', fit_option, '', fit_min, fit_max)
    c.Modified()
    c.Update()
    c.SaveAs('{0}.png'.format(path))
    
    chi2 = float(fit_f.GetChisquare()) / fit_f.GetNDF()
    tau = fit_f.GetParameter(1)
    tau_err = fit_f.GetParError(1)
    
    histo.Write('fitted_histogram')
    
    out_file.Close()
    
    del fit_f
    del histo
    del c
    
    return tau, tau_err, chi2
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Plot lifetime histogram')
    parser.add_argument('-i', '--inputFile', dest='inputFile', help='.root input file path (without extension)', default='./test', type=str)
    parser.add_argument('-t0', '--threshold0', dest='threshold0', help='Pulse lower threshold (channel 0)', default=1200., type=float)
    parser.add_argument('-t1', '--threshold1', dest='threshold1', help='Pulse lower threshold (channel 1)', default=1200., type=float)
    parser.add_argument('-r', '--rate', dest='rate', help='Digitizer sampling rate (in MHz)', default=250., type=float)
    parser.add_argument('-b', '--bins', dest='bins', help='Histogram number of bins', default=50, type=int)
    parser.add_argument('-m', '--maxt', dest='maxt', help='Max t in the histogram', default=10., type=float)
    parser.add_argument('-f', '--fmin', dest='fmin', help='Min t in the fit', default=0., type=float)
    parser.add_argument('-L', '--likelihood', action='store_true', help='Fit by means of maximum likelihood method')
    args = parser.parse_args()
    
    print '\nInput path:\t\t\t', '{0}.root'.format(args.inputFile)
    print 'Channel 0 threshold:\t\t', args.threshold0
    print 'Channel 1 threshold:\t\t', args.threshold1
    print 'Digitizer rate:\t\t\t', '{0} MHz'.format(args.rate)
    print 'Histogram number of bins:\t', args.bins
    print 'Min t in the fit:\t\t', args.fmin
    print 'Max t in the histogram:\t\t', args.maxt, '\n'
    
    t_up, t_down = events_partition(args.inputFile + '.root', args.rate)
    
    if args.likelihood:
        fit_opt = 'L'
        print '\nTrying to fit by means of binned likelihood method\n'
    else:
        fit_opt = '1'
        print '\nTrying to fit by means of chi square method\n'
        
    ROOT.gStyle.SetOptStat(11)
    ROOT.gStyle.SetOptFit(1112)
    
    tau, tau_err, chi2 = makePlot (t_up, '#mu up - {0} bin'.format(args.bins), args.bins, 0., args.maxt, fit_opt, args.fmin, args.maxt, 'up_{0}bin_{1}fitmin'.format(args.bins, args.fmin))
    
    stability = open ('stability.txt', 'w+')
    for i in range(41):
        bins = args.bins + i*5
        for j in range(1,21):
            fmin = j*0.125
            fmax = args.maxt - j*0.125
            frange = args.maxt - j*0.25
            tau, tau_err, chi2 = makePlot (t_down, '#mu down - {0} bin'.format(bins), bins, 0., args.maxt, fit_opt, fmin, fmax, 'down_{0}bin_{1}range'.format(bins, frange))
            stability.write(str(bins)+'\t'+str(frange)+'\t'+str(chi2)+'\t'+str(tau)+'\t'+str(tau_err)+'\n')
            print '\nbins: {0} -- fit range: {1} correctly written\n'.format(bins, frange)
    
    stability.close()

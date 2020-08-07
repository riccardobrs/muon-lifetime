import argparse
import ROOT
import numpy as np
from math import *

def f_exp(x,amp,tau):
	return amp * exp (- x / tau )
	
def makePulls(histo, fit_f, fit_option, fit_min, fit_max, N_bin, path,name):

	out_file = ROOT.TFile('{0}.root'.format(path), 'RECREATE')    
	histo.Write('histogram')
	fit_f.Write('fit_function')
    
	c = ROOT.TCanvas()
	c.cd()
	histo.Draw()
	histo.Fit(fit_f, fit_opt, '', fit_min, fit_max)
	amp = fit_f.GetParameter(0)
	tau = fit_f.GetParameter(1)
	c.Modified()
	c.Update()
	c.SaveAs('{0}.png'.format('fitted histo'))
    
	histo.Write('fitted_histogram')
    	

	print('amp= ', amp, '\n')
	print('tau= ', tau, '\n')   
	
	hpull = ROOT.TH1D('Statistical box', 'pull histo {0} events '.format(name), N_bin, -5, 5.)
	fit_gaus = ROOT.TF1('fit_gaus', 'gaus', 0., 0.) 
	fit_gaus.SetParameter(0, 10)
	fit_gaus.SetParameter(1, 1) 
	fit_gaus.SetParameter(0, 1.3)  
    
    
	pulls = np.array([])
	
	dim = histo.GetNbinsX()
	for i in range(1, dim):
		if histo.GetBinContent(i) != 0 :
			pull_value = ( histo.GetBinContent(i) - fit_f.Eval(histo.GetBinCenter(i)) ) / sqrt(histo.GetBinContent(i))
			pulls = np.append(pulls, pull_value)
    
	for j in range(0, np.size(pulls) ):
		hpull.Fill(pulls[j])
		
	hpull.Write('pull histogram')
	hpull.GetXaxis().SetTitle('pull')
	hpull.GetYaxis().SetTitle('Counts')
	fit_gaus.Write('gaus_fit_function')
    
	c = ROOT.TCanvas()
	c.cd()
	hpull.Draw()
	hpull.Fit(fit_gaus, 'L', '', -5., 5.)
	amp = fit_gaus.GetParameter(0)
	mean = fit_gaus.GetParameter(1)
	sigma = fit_gaus.GetParameter(2)
	c.Modified()
	c.Update()
	c.SaveAs('{0}.png'.format(path))
    
	print('amp = ', amp, '\n')
	print('mean = ', mean, '\n')
	print('sigma = ', sigma, '\n')   
    
	hpull.Write('fitted_pull_histogram')
	
	return
	
if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Plot lifetime histogram')
	parser.add_argument('-i', '--inputFile', dest='inputFile', help='.root input file path (without extension)', default='./test', type=str)
	parser.add_argument('-t0', '--threshold0', dest='threshold0', help='Pulse lower threshold (channel 0)', default=1200., type=float)
	parser.add_argument('-t1', '--threshold1', dest='threshold1', help='Pulse lower threshold (channel 1)', default=1200., type=float)
	parser.add_argument('-r', '--rate', dest='rate', help='Digitizer sampling rate (in MHz)', default=244., type=float)
	parser.add_argument('-b', '--bins', dest='bins', help='Histogram number of bins', default=50, type=int)
	parser.add_argument('-m', '--maxt', dest='maxt', help='Max t in the histogram', default=11., type=float)
	parser.add_argument('-f', '--fmin', dest='fmin', help='Min t in the fit', default=0., type=float)
	parser.add_argument('-L', '--likelihood', action='store_true', help='Fit by means of maximum likelihood method')
	args = parser.parse_args()
    
	print('\nInput path:\t\t\t', '{0}.root'.format(args.inputFile))
	print('Channel 0 threshold:\t\t', args.threshold0)
	print('Channel 1 threshold:\t\t', args.threshold1)
	print('Digitizer rate:\t\t\t', '{0} MHz'.format(args.rate))
	print('Histogram number of bins:\t', args.bins)
	print('Min t in the fit:\t\t', args.fmin)
	print('Max t in the histogram:\t\t', args.maxt, '\n')
	
	
	ROOT.gStyle.SetOptStat(11)
	ROOT.gStyle.SetOptFit(1112)    
    
	h_overall = ROOT.TH1D()
	fit_f_overall = ROOT.TF1()
	
	h_up = ROOT.TH1D()
	fit_f_up = ROOT.TF1()
	
	h_down = ROOT.TH1D()
	fit_f_down = ROOT.TF1()
	
	
    
	f_overall = ROOT.TFile('lifetime_overall.root', 'READ') 
	ROOT.gDirectory.GetObject('histogram', h_overall)
	ROOT.gDirectory.GetObject('fit_function', fit_f_overall)
	out_file_overall = ROOT.TFile('{0}.root'.format('pull_overall'), 'RECREATE')
	
	f_up = ROOT.TFile('lifetime_up.root', 'READ') 
	ROOT.gDirectory.GetObject('histogram', h_up)
	ROOT.gDirectory.GetObject('fit_function', fit_f_up)
	out_file_up = ROOT.TFile('{0}.root'.format('pull_up'), 'RECREATE')
	
	f_down = ROOT.TFile('lifetime_down.root', 'READ') 
	ROOT.gDirectory.GetObject('histogram', h_down)
	ROOT.gDirectory.GetObject('fit_function', fit_f_down)
	out_file_down = ROOT.TFile('{0}.root'.format('pull_down'), 'RECREATE')
    
	
	
	if args.likelihood:
		fit_opt = 'L'
		print('\nTrying to fit by means of binned likelihood method\n')
	else:
		fit_opt = '1'
		print('\nTrying to fit by means of chi square method\n')
	
	#N_bin_overall = 15
	#N_bin_up = 11
	#N_bin_down = 15
	
	N_bin_overall = 10
	N_bin_up = 10
	N_bin_down = 9
	
	makePulls(h_overall, fit_f_overall, fit_opt, args.fmin, args.maxt, N_bin_overall, 'lifetime_overall','overall')
	makePulls(h_up, fit_f_up, fit_opt, args.fmin, args.maxt, N_bin_up, 'lifetime_up','up')
	makePulls(h_down, fit_f_down, fit_opt, args.fmin, args.maxt, N_bin_down, 'lifetime_down','down')
    	
				
	out_file_overall.Close()
	out_file_up.Close()
	out_file_down.Close()

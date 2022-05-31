import csv
import io
import ROOT
from math import *
from glob import glob
import os
from statistics import stdev

'''
this script requires that CSV files to be stored in directories named as *_ns
where * is the nominal delay value. Example of correct folder structure:

    DelayLinearity
        DelayLinearity.py
        3_5_ns
            file1.CSV
            file2.CSV
            etc...
        20_ns
            file1.CSV
            file2.CSV
            etc...        
'''

def FromCSVToDelay(CSV_Name, N, FileName):
    
    ROOT.gStyle.SetOptFit(1112)
    
    print CSV_Name, ' is going to be processed'
    
    HowManyPoints = 50

    HalfRise1 = -0.36
    Delta1 = abs(HalfRise1)
    HalfRise2 = -0.36
    Delta2 = abs(HalfRise2)

    c = ROOT.TCanvas('c{0}'.format(N), '')
    gr1 = ROOT.TGraph()
    gr2 = ROOT.TGraph()
    fit1 = ROOT.TGraph()
    fit2 = ROOT.TGraph()

    gr1.GetXaxis().SetTitle('t (s)')
    gr1.GetYaxis().SetTitle('V (V)')
    gr1.SetMarkerColor(ROOT.kRed)
    gr1.SetMarkerStyle(20)
    gr1.SetMarkerSize(0.6)

    gr2.SetMarkerColor(ROOT.kBlue)
    gr2.SetMarkerStyle(20)
    gr2.SetMarkerSize(0.6)

    ReadStarter = False

    with io.open(CSV_Name, newline='') as csvfile:
        readlines = csv.reader(csvfile, delimiter=' ', quotechar='|')
        
        i = 0
        for row in readlines:
            if ReadStarter and not len(row)==0:
                SplittedLine = (','.join(row)).split(',')
                gr1.SetPoint(i, float(SplittedLine[0]), float(SplittedLine[1]))
                gr2.SetPoint(i, float(SplittedLine[0]), float(SplittedLine[2]))
                if abs(HalfRise1-float(SplittedLine[1])) < Delta1 and Delta1 > 0.15:
                    Delta1 = abs(HalfRise1-float(SplittedLine[1]))
                    HalfRise1_index = i
                if abs(HalfRise2-float(SplittedLine[2])) < Delta2 and Delta2 > 0.15:
                    Delta2 = abs(HalfRise2-float(SplittedLine[2]))
                    HalfRise2_index = i
                i += 1
            if 'TIME' in ','.join(row):
                ReadStarter = True
                
    xi = ROOT.Double()
    xf = ROOT.Double()
    x0 = ROOT.Double()
    y0 = ROOT.Double()
    yi = ROOT.Double()
    yf = ROOT.Double()

    c.cd()
    gr1.Draw('AP')
    gr2.Draw('P SAME')
    fit1.Draw('P SAME')
    fit2.Draw('P SAME')
    '''
    gr1.GetPoint(HalfRise1_index-1, xi, yi)
    gr1.GetPoint(HalfRise1_index, x0, y0)
    gr1.GetPoint(HalfRise1_index+1, xf, yf)
    fit1.SetPoint(0, xi, yi)
    fit1.SetPoint(1, x0, y0)
    fit1.SetPoint(2, xf, yf)
    f1 = ROOT.TF1('linear1', '[0]+[1]*v', xi, xf)
    '''
    gr1.GetPoint(HalfRise1_index, x0, y0)
    fit1.SetPoint(0, x0, y0)
    for j in range(1,HowManyPoints):
        gr1.GetPoint(HalfRise1_index-j, xi, yi)
        gr1.GetPoint(HalfRise1_index+j, xf, yf)
        fit1.SetPoint(2*j-1, xi, yi)
        fit1.SetPoint(2*j, xf, yf)
    f1 = ROOT.TF1('FD1', '([0]/(exp([1]*(v-[2]))+1))+[3]', xi, xf)
    f1.SetLineColor(ROOT.kRed)
    f1.SetLineWidth(1)
    '''
    gr2.GetPoint(HalfRise2_index-1, xi, yi)
    gr2.GetPoint(HalfRise2_index, x0, y0)
    gr2.GetPoint(HalfRise2_index+1, xf, yf)
    fit2.SetPoint(0, xi, yi)
    fit2.SetPoint(1, x0, y0)
    fit2.SetPoint(2, xf, yf)
    f2 = ROOT.TF1('linear2', '[0]+[1]*v', xi, xf)
    '''
    gr2.GetPoint(HalfRise1_index, x0, y0)
    fit2.SetPoint(0, x0, y0)
    for j in range(1,HowManyPoints):
        gr2.GetPoint(HalfRise2_index-j, xi, yi)
        gr2.GetPoint(HalfRise2_index+j, xf, yf)
        fit2.SetPoint(2*j-1, xi, yi)
        fit2.SetPoint(2*j, xf, yf)
    f2 = ROOT.TF1('FD2', '([0]/(exp([1]*(v-[2]))+1))+[3]', xi, xf)
    f2.SetLineColor(ROOT.kBlue)
    f2.SetLineWidth(1)
    
    f1.SetParameter(0, 0.7)
    f1.SetParameter(1, 1e+07)
    f1.SetParameter(2, -8e-08)
    f1.SetParameter(3, -0.7)
    f2.SetParameter(0, 0.7)
    f2.SetParameter(1, 1e+07)
    f2.SetParameter(2, -8e-08 + float(CSV_Name.split('/')[0].replace('_ns','').replace('_','.'))*1e-09)
    f2.SetParameter(3, -0.7)
    
    fit1.Fit('FD1')
    fit2.Fit('FD2')
    
    x1 = f1.GetParameter(2) + log((f1.GetParameter(0) / (HalfRise1 - f1.GetParameter(3))) -1) / f1.GetParameter(1)
    x2 = f2.GetParameter(2) + log((f2.GetParameter(0) / (HalfRise2 - f2.GetParameter(3))) -1) / f2.GetParameter(1)
    #delay = (-0.36-f2.GetParameter(0))/f2.GetParameter(1) - (-0.36-f1.GetParameter(0))/f1.GetParameter(1)
    delay = abs(x1-x2)

    print '''
********************************************
  Experimental delay = {0} s
********************************************
    '''.format(delay)
    
    c.SaveAs(FileName)

    return c, delay


if __name__ == '__main__':
    
    ROOT.gStyle.SetOptFit(1112)
    
    x_list = []
    y_list = []
    y_err_list = []
    i = 1
    
    directories = glob('*_ns')
    
    for directory in directories:
        
        x_list.append(float(directory.replace('_', '.').replace('.ns', '')))
        y = 0.
        calc_err = []
        j = 1
        CSVs = glob(directory+'/*.CSV')
        
        for CSV_path in CSVs:
            rootName = 'measure_{0}.root'.format(j)
            canva, delay = FromCSVToDelay(CSV_path, i, rootName)
            os.system('mv {1} {0}/{1}'.format(directory, rootName))
            y += delay*1e+09
            calc_err.append(delay*1e+09)
            i += 1
            j += 1
        
        y_list.append(y/len(CSVs))
        y_err_list.append(stdev(calc_err))
    
    c = ROOT.TCanvas()
    g = ROOT.TGraphErrors()
    g.SetMarkerStyle(20)
    g.SetMarkerSize(0.8)
    g.SetMarkerColor(ROOT.kBlue)
    g.GetXaxis().SetTitle('Nominal Delay (ns)')
    g.GetYaxis().SetTitle('Experimental Delay (ns)')
    
    i = 0
    for x in x_list:
        g.SetPoint(i, x, y_list[i])
        g.SetPointError(i, 0, y_err_list[i])
        i += 1
    
    f = ROOT.TF1('linear', '[0]+[1]*v', min(x_list), max(x_list))
    f.SetParName(0, 'A')
    f.SetParName(1, 'B')
    
    FitResult = ROOT.TFitResultPtr()
    CovMatrix = ROOT.TMatrixDSym()
    
    FitResult = g.Fit('linear', 'sames')
    CovMatrix = FitResult.GetCovarianceMatrix()
    print'''
***************************
***  Covariance Matrix  ***
***************************
    ''', CovMatrix[0][0], '   ', CovMatrix[0][1], '''
    ''', CovMatrix[1][0], '   ', CovMatrix[1][1]
    
    c.cd()
    g.Draw('AP')
    c.SaveAs('DelayLinearity.root')
    c.SaveAs('DelayLinearity.png')
    

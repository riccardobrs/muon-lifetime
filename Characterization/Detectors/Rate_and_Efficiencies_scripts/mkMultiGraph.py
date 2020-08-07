#!/usr/bin/env python

'''
Ignore the first line (#!/usr/bin/env python): it's a directive for your command line interpreter on how it should execute a script.
In order to execute the script you must run the following (if you want to use default parser options):

    python mkMultiGraph.py
    
If you want to assign to parser options values different from the default ones, you must run:

    python mkMultiGraph.py --inputRootFile=your_input_TFile_name --InputTxtFile=your_input_txtFile_name etc..
    
Note that if you specify only some parser options, the remaining ones are set to their default values.
'''

import sys
argv = sys.argv
sys.argv = argv[:1]
import optparse
from math import *
import ROOT as rt
import LabLib as Lib

if __name__ == '__main__':
    
    print '''
-----------------------------------------------------------------------------------------------------
                        __       ____
     \  |           | _ __|  ^  |  _                       |          \  |         |
    |\/ | | | | | | | | |   | | | (      __|   _` |  |__   |__       |\/ |   _` |  |  /   _ \   __|
    |   | | |_| | | | | |   | | |   __  |     (   |   __)   _  )     |   |  (   |    <    __/  |
   _|  _| |_____| |_| |_|   | | |____| _|    \__,_|  |    _| | |    _|  _| \__,_| _|\_\ \___| _| 
                                                    _|
-----------------------------------------------------------------------------------------------------
    '''
    
    sys.argv = argv
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--RateVs'     		, dest='RateVs'      	, help='decide if RateVsThreshold or RateVsBias mode'      	   		, default='Threshold'                   )
    parser.add_option('--line'              , dest='line'           , help='non-mandatory TGraphPainter Draw() option. AP already set'  , default='NO'                          ) #Ref: https://root.cern.ch/doc/master/classTGraphPainter.html
    parser.add_option('--grid'              , dest='grid'           , help='draw grid on canva'                                         , default=0 ,       type=float          ) #0=False, 1=True
    parser.add_option('--markerSize'        , dest='markerSize'     , help='set marker size'                                            , default=0.75,       type=float        )
    
    (opt, args) = parser.parse_args()

    print '                            RateVs =', opt.RateVs            
    if opt.line == 'NO':
        print '                                line = not drawn'
    else:
        print '                                line = drawn with', opt.line, 'option'
    if opt.grid == 0:
        print '                                grid = not drawn'
    else:
        print '                                grid = drawn on canvas'
    print '                         marker size =', opt.markerSize
    
    if opt.RateVs == 'Threshold':
    	inputTxtFile = 'DetectorsVoltage.txt'
    	inputRootFile = 'DetectorsVoltage.root'
    	TDirectoryName = 'RateVsThreshold'
    	XaxisTitle = 'Threshold (mV)'
    elif opt.RateVs == 'Voltage':
    	inputTxtFile = 'DetectorsThreshold.txt'
    	inputRootFile = 'DetectorsThreshold.root'
    	TDirectoryName = 'RateVsVoltage'
    	XaxisTitle = 'Bias (V)'
    
    markerStyle = [20, 22, 21, 23, 29, 47, 45, 43, 41, 39, 34, 33] #Ref: https://root.cern.ch/doc/master/classTAttMarker.html
    markerColor = [ rt.kBlue+2, rt.kRed+1, rt.kGreen+2, rt.kPink, rt.kOrange+1, \
                    rt.kSpring-8, rt.kAzure+1, rt.kViolet-5, rt.kCyan-1, rt.kYellow-2, \
                    rt.kYellow+4, rt.kRed-9]
    
    with open(inputTxtFile, 'r') as in_txt:
    	lines = in_txt.readlines()
    
    dtc1 = 'default'
    dtc2 = 'default'
    dtc3 = 'default'
    subdir1 = []
    subdir2 = []
    subdir3 = []
    
    i = 0
    for line in lines:
        if i != 0:
            array_line = line.split()
            if (dtc1 == 'default' and dtc2 == 'default' and dtc3 == 'default') or dtc1 == array_line[0]:
                dtc1 = array_line[0]
                subdir1.append(array_line[1])
            elif (dtc1 != 'default' and dtc1 != array_line[0] and dtc2 == 'default' and dtc3 == 'default') or dtc2 == array_line[0]:
                dtc2 = array_line[0]
                subdir2.append(array_line[1])
            elif (dtc1 != 'default' and dtc1 != array_line[0] and dtc2 != 'default' and dtc2 != array_line[0] and dtc3 == 'default') or dtc3 == array_line[0]:
                dtc3 = array_line[0]
                subdir3.append(array_line[1])
        i += 1
    
    detectors = {}
    if len(subdir1) != 0:
        detectors[dtc1] = subdir1
    if len(subdir2) != 0:
        detectors[dtc2] = subdir2
    if len(subdir3) != 0:
        detectors[dtc3] = subdir3
        
    rt.gROOT.SetBatch()
    in_root = rt.TFile(inputRootFile, 'READ')
    
    multi1 = rt.TMultiGraph()
    multi2 = rt.TMultiGraph()
    multi3 = rt.TMultiGraph()
	
    multi1.GetXaxis().SetTitle(XaxisTitle)
    multi2.GetXaxis().SetTitle(XaxisTitle)
    multi3.GetXaxis().SetTitle(XaxisTitle)
    multi1.GetYaxis().SetTitle('Rate (Hz)')
    multi2.GetYaxis().SetTitle('Rate (Hz)')
    multi3.GetYaxis().SetTitle('Rate (Hz)')
    
    i = 0
    for dtc in detectors.keys():
        #print 'key ', dtc, '=', detectors[dtc] #to control if the detectors dictionary is correct
        if i == 0:
            rt.gDirectory.cd(dtc)
        else:
            rt.gDirectory.cd('../../'+dtc)
        j = 0
        while True:
            if j == 0:
                rt.gDirectory.cd(detectors[dtc][j])
            else:
                rt.gDirectory.cd('../'+detectors[dtc][j])

            gr = rt.gDirectory.Get(TDirectoryName)

            gr.SetMarkerStyle(markerStyle[j])
            gr.SetMarkerColor(markerColor[j])
            gr.SetMarkerSize(opt.markerSize)
	    gr.SetName(detectors[dtc][j])
            if i == 0:
                multi1.Add(gr)
            elif i == 1:
                multi2.Add(gr)
            elif i == 2:
                multi3.Add(gr)
            j += 1
            if j == len(detectors[dtc]):
                break
        i += 1
    
    in_root.Close()
    
    if opt.line == 'NO':
        drawOpt = 'AP'
    else:
        drawOpt = 'AP'+opt.line
    
    for i in range(0, len(detectors.keys())):
        c = Lib.create_canva(i)
        c.cd()
        if i == 0:
            multi1.Draw(drawOpt)
        elif i == 1:
            multi2.Draw(drawOpt)
        elif i == 2:
            multi3.Draw(drawOpt)
        if opt.grid == 1:
            c.SetGrid()
	c.BuildLegend()
        c.SaveAs(detectors.keys()[i]+'.png')
	c.SaveAs(detectors.keys()[i]+'.root')
        i += 1     

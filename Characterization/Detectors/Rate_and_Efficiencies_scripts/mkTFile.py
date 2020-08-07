#!/usr/bin/env python

'''
Ignore the first line (#!/usr/bin/env python): it's a directive for your command line interpreter on how it should execute a script.
In order to execute the script you must run the following (if you want to use default parser options):

    python mkTFile.py
    
If you want to assign to parser options values different from the default ones, you must run:

    python mkTFile.py --inputFile=your_input_file_name --outputFile=your_output_file_name
    
Note that if you specify only one parser option, the remaining ones are set to their default values.
'''

import sys
argv = sys.argv
sys.argv = argv[:1]
import optparse
from math import *
import ROOT as rt
from io import StringIO
import numpy as np
import LabLib as Lib

if __name__ == '__main__':
    
    print '''
-------------------------------------------------------------------------
                
    _ __|   __|  '    |               \  |         |
    | |    |_   | | | |   _ \        |\/ |   _` |  |  /   _ \   __|
    | |     _|  | | | |   __/        |   |  (   |    <    __/  |
    |_|  |_|    | | |_| \___|       _|  _| \__,_| _|\_\ \___| _| 
                                                  
-------------------------------------------------------------------------
    '''
    print '''
Important: the TFile is organized in directories corresponding to each detector and subdirectories corresponding to the power supply voltage

    TFile
      |___Detector1
      |         |___900V
      |         |___1000V
      |         |___ etc...
      |
      |___Detector2
      |         |___1000V
      |         |___etc...
      |
      |___Detector3
                |___1000V
                |___etc...
'''
    
    sys.argv = argv
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--RateVs'     	, dest='RateVs'      	, help='decide if RateVsThreshold or RateVsBias mode'      	   , default='Threshold'                     )
    
    (opt, args) = parser.parse_args()
    
    print '                            RateVs =', opt.RateVs
    
    rt.gROOT.SetBatch()
    
    if opt.RateVs == 'Threshold':
    	inputFile = 'DetectorsVoltage.txt'
    	outputFile = 'DetectorsVoltage.root'
    	TDirectoryName = 'RateVsThreshold'
    elif opt.RateVs == 'Voltage':
    	inputFile = 'DetectorsThreshold.txt'
    	outputFile = 'DetectorsThreshold.root'
    	TDirectoryName = 'RateVsVoltage'
    
    with open(inputFile, 'r') as in_file: #file opened in read mode
    	files = in_file.readlines()    
    
    out_file = rt.TFile(outputFile, 'RECREATE') #Create a new file, if the file already exists it will be overwritten. 
    
    if not out_file.IsOpen():
        print 'Warning: some errors occured while trying to open', outputFile
    
    else:
        
        print '\n', outputFile, 'successfully opened \n'
    
        j = 0
        for row in files:

            if j != 0:
            
		dtc_volt = row.split()
                gr = Lib.readTxt(dtc_volt[0]+'_'+dtc_volt[1]+'.txt')

                rt.gDirectory.mkdir(dtc_volt[0])
                rt.gDirectory.cd(dtc_volt[0])
                rt.gDirectory.mkdir(dtc_volt[1])
                rt.gDirectory.cd(dtc_volt[1])
                print 'Directory {0}/{1} has been successfully created'.format(dtc_volt[0],dtc_volt[1])
                
                gr.Write(TDirectoryName)
                print 'TGraphErrors has been correctly written in the TFile \n'
		rt.gDirectory.cd('../..')
            
            j += 1
            
        out_file.Close()
        print outputFile, 'successfully closed'

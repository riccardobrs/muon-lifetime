import argparse
from bs4 import BeautifulSoup
import numpy as np
import os
import re
import ROOT


def GetXArray(Y, rate):
    X = []

    i = 1
    for y in Y:
        X.append(float(i) / rate)
        i += 1

    return np.array(X)


def BuildTGraph(X, Y):
    gr = ROOT.TGraph()
    gr.GetXaxis().SetTitle('time [#mus]')

    i = 0
    for x in X:
        gr.SetPoint(i, float(X[i]), float(Y[i]))
        i += 1

    return gr


'''
return an output dictionary where values are TGraph built from text y values
of the input dictionary given the sampling rate
'''
def BuildDictionary(in_Dict, rate):
    
    out_Dict = {}

    for key in in_Dict.keys():
        
        x0_list, y0_list = [], []
        
        l = re.split(' |\n', in_Dict[key])
        #build sample lists
        y0_list.extend(l[:(len(l) - 2)])  # the last 2 elements of the list are '' instead of numbers
        x0_list = GetXArray(y0_list, rate)
        #build output dictionary
        out_Dict[key] = BuildTGraph(x0_list, y0_list)
        
    return out_Dict

'''
TFile is built with one folder for each event.
Inside each folder channels TGraph are stored
'''
def BuildTFile(ch0, ch1, ch2, ch3):
    
    for key in ch0.keys():
        
        folder_name = 'Event{0}'.format(key)
        ROOT.gDirectory.mkdir(folder_name)
        ROOT.gDirectory.cd(folder_name)
        #print 'Directory {0} successfully created'.format(folder_name)
        ch0[key].Write('channel0')
        if key in ch1.keys():
            ch1[key].Write('channel1')
        if key in ch2.keys():
            ch2[key].Write('channel2')
        if key in ch3.keys():
            ch3[key].Write('channel3')
        ROOT.gDirectory.cd('..')
    
    print '\nTFile successfully built'

'''
XML parsing
'''
def parseXML(xmlsoup, rate, tfile_name, tfile_opt):
    
    ch0 = {}
    ch1 = {}
    ch2 = {}
    ch3 = {}
    
    ch0_acquired = False
    ch1_acquired = False
    ch2_acquired = False
    ch3_acquired = False
    
    N_events = 0
    
    for event in xmlsoup.find_all('event'):
        
        for subevent in event.find_all('trace'):
            
            N_events += 1
            
            if subevent.attrs['channel'] == '0':
                ch0[event.attrs['id']] = subevent.text
                ch0_acquired = True
            elif subevent.attrs['channel'] == '1':
                ch1[event.attrs['id']] = subevent.text
                ch1_acquired = True
            elif subevent.attrs['channel'] == '2':
                ch2[event.attrs['id']] = subevent.text
                ch2_acquired = True
            elif subevent.attrs['channel'] == '3':
                ch3[event.attrs['id']] = subevent.text
                ch3_acquired = True
  
    if ch0_acquired and ch1_acquired and not (ch2_acquired or ch3_acquired):
        N_events /= 2
    if ch0_acquired and ch1_acquired and ch2_acquired and not ch3_acquired:
        N_events /= 3
    if ch0_acquired and ch1_acquired and ch2_acquired and ch3_acquired:
        N_events /= 4    
    
    print '\nNumber of triggered events: ', N_events
    print '\nChannel 0 acquisition: ', ch0_acquired
    print 'Channel 1 acquisition: ', ch1_acquired
    print 'Channel 2 acquisition: ', ch2_acquired
    print 'Channel 3 acquisition: ', ch3_acquired

    ch0 = BuildDictionary(ch0, rate)
    ch1 = BuildDictionary(ch1, rate)
    ch2 = BuildDictionary(ch2, rate)
    ch3 = BuildDictionary(ch3, rate)

    out_file = ROOT.TFile(tfile_name, tfile_opt)
    BuildTFile(ch0, ch1, ch2, ch3)
    out_file.Close()


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Build .root output from .xml input -- default options can be modified')
    parser.add_argument('-v', '--xml', dest='xmlName', help='.xml input file path (without extension)', default='./test', type=str)
    parser.add_argument('-r', '--rate', dest='rate', help='Digitizer sampling rate (in MHz)', default=250., type=float)
    args = parser.parse_args()
    
    inputname = '{0}.xml'.format(args.xmlName)
    outputname = '{0}.root'.format(args.xmlName)
    
    print '\nInput path:\t\t', inputname
    print 'Ouput path:\t\t', outputname
    print 'Digitizer rate:\t\t', args.rate, 'MHz'
    
    print '\nTrying to read', inputname
    
    rowindex = 1
    rowmax = 50000
    subxml = 1
    list_xml = ['f1.xml']
    
    with open(inputname, 'r') as in_xml:
        
            for line in in_xml.readlines():
                with open('f{0}.xml'.format(subxml), 'a+') as in_subxml:
                    in_subxml.write(line)
                    if rowindex > rowmax and '/event' in line:
                        subxml += 1
                        rowindex = 0
                        list_xml.append('f{0}.xml'.format(subxml))
                rowindex += 1
    
    tfile_mode = 'RECREATE'
    
    for x in list_xml:
        with open(x, 'r') as in_subxml:
            contents = in_subxml.read()
        soup = BeautifulSoup(contents, 'lxml')
        print 'xml content correctly get'
        parseXML(soup, args.rate, outputname, tfile_mode)
        tfile_mode = 'UPDATE'
        os.system('rm {0}'.format(x))
        

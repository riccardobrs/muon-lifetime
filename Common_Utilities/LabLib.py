from math import *
import numpy as np
from io import StringIO
import ROOT as rt
import os

def create_canva (N):
    return rt.TCanvas('c{}'.format(N), "", 100, 200, 700, 500)

#given a number and its error this function return the correct round values
def roundNumErr(num, err):
    
    val = {}
    times = 0
    x_err = float(err)
    
    if err < 1:
        
        while True:
            x_err *= 10
            times += 1
            if x_err >= 1:
                break
        if x_err < 1.95:
            times += 1
        elif x_err > 9:
            times += -1
    
    elif err >= 19.5:
        
        while True:
            x_err /= 10
            times += -1
            if x_err < 20:
                break  
        if x_err >= 19.5:
            times += -1
    
    elif err >= 1 and err < 1.95:
        
        times = 1
        
    elif err >= 1.95 and err < 19.5:
        
        times = 0
    
    i=30
    while i >= times:
        
        num = round(float(num),i)
        err = round(float(err),i)
        i += -1
    
    val['num']=num
    val['err']=err
    
    return val
        
    
    
#weightedMean function takes array_x as value array and array_x_err as errors array and returns a dictionay with keys 'mean' and 'err'    
def weightedMean(array_x, array_x_err, mode):

    val = {} #dictionary initialized
        
    if len(array_x) <= len(array_x_err) and mode == 'ric':
        
        num = 0.
        den = 0.
        
        array_x = np.array(array_x) #array arguments are casted into numpy arrays
        array_x_err = np.array(array_x_err)
        
        i=0
        for x in array_x:
            num += x/(array_x_err[i]**2)
            den += 1/(array_x_err[i]**2)
            i += 1
        
        val['mean'] = float(num)/den #numerator casted to float
        val['err'] = 1./sqrt(den)
        
    elif len(array_x) > len(array_x_err) and mode == 'ric':
        
        print 'Warning: errors will be assigned equal to 0'
        val['mean'] = np.mean(array_x)
        val['err'] = 0.
        
    elif mode == 'fil':
    
        val['mean'] = np.mean(array_x)
        val['err'] = sqrt(np.mean(array_x))
    
    return val
    
#generate a txt renamed as 'latex'+fileName useful to latex table creation
def latexTxt(fileName):

    data_file = open(fileName, 'r') #file opened in read mode
    rows = data_file.readlines() #return an array of lines
    data_file.close()
    
    outName = 'latex_{0}'.format(fileName)
    
    i=0
    for line in rows:
        
        if i != 0: #first line contains columns description
            
            array_line = np.genfromtxt(StringIO(u'{}'.format(line))) #StringIO argument need to have unicode as first
            
            j=0
            for num in array_line:
                if j==0:
                    outString = '$'+str(num)+'$'
                else:
                    outString = outString + '\t&\t$' + str(num)+'$'
                j+=1
                
            if len(outString.split('&')) < 5:
                
                diff = 5-len(outString.split('&'))
                for n in range(0,diff):
                    outString = outString + '\t&\t//'
                    
            mean = weightedMean(array_line[2:],np.sqrt(array_line[2:]), 'fil')['mean']
            rate = float(mean)/array_line[1]
            err = weightedMean(array_line[2:],np.sqrt(array_line[2:]), 'fil')['err']
            rate_err = float(err)/array_line[1]
            outString = outString +'\t&\t$'+str(roundNumErr(rate,rate_err)['num'])+'$\t&\t$'+str(roundNumErr(rate,rate_err)['err'])+'$\t\\\\\n'
            
            with open(outName, 'a') as outfile:
                outfile.write(outString)
                #note that the 'with' statement ensure outfile to be automatically closed
                
        else:
            
            with open(outName, 'w') as outfile:
                outfile.write(line.replace('\n','')+'\tRate (Hz)\tRate_error (Hz)\n@CommodoroLuca creati l\'intestazione che vuoi\n')
                
        i+=1 

#generate all 'latex'+fileName from one only DetectorsVoltage.txt file
def GenAllLatex(configFile):
    with open(configFile, 'r') as in_file:
        rows = in_file.readlines()
    i=0
    for line in rows:
        if i!=0:
            array_line = line.split()
            latexTxt(array_line[0]+'_'+array_line[1]+'.txt')
            print 'latex_'+array_line[0]+'_'+array_line[1]+'.txt correctly created'
        i+=1
    
#given a .txt input file with v values in column1 and count values in the other columns, readTxt function return the corresponding TGraphErrors
def readTxt (fileName):
    
    gr = rt.TGraphErrors()
    data_file = open(fileName, 'r') #file opened in read mode
    
    rows = data_file.readlines() #return an array of lines
    
    i=0
    for line in rows:
        
        if i != 0: #first line contains columns description
            
            array_line = np.genfromtxt(StringIO(u'{}'.format(line))) #StringIO argument need to have unicode as first character
            array_err = np.sqrt(array_line)
            
            gr.SetPoint(i-1, array_line[0], float(weightedMean(array_line[2:], array_err, 'fil')['mean'])/array_line[1])
            gr.SetPointError(i-1, 0., float(weightedMean(array_line[2:], array_err, 'fil')['err'])/array_line[1]) #threshold voltage error is now set to 0 (maybe to be set to non-zero value ?)
            
        i += 1
            
    data_file.close()   
    
    return gr

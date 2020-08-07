#python3 compute_efficiencies.py

'''
the input txt files have the following columns order:
Triple  Double  Eff_g   Eff_g_err
'''

import glob
import numpy as np
from io import *
from math import *
import os

                
def efficiency(txtfile):
    
    outName = txtfile.replace('.txt', '_processed.txt')
    
    file_content = np.loadtxt(txtfile)
    
    out_content = np.zeros((file_content.shape[0], file_content.shape[1]+3)) #add eff, eff_err_stat and eff_err_syst columns
    out_content[:,:-3] = file_content
    out_content[:,4] = file_content[:,0] / (file_content[:,1]*file_content[:,2])
    out_content[:,5] = np.sqrt(file_content[:,0] * (1 - file_content[:,0]/ (file_content[:,1]*file_content[:,2]) )) / (file_content[:,1]*file_content[:,2])
    out_content[:,6] = file_content[:,0]*file_content[:,3] / ( file_content[:,1]*file_content[:,2]*file_content[:,2] )
        
    np.savetxt(outName, out_content, header='Triple\tDouble\t\tEff_g\t\tEff_g_err\tEff\t\tEff_err_stat\tEff_err_syst', delimiter='\t', fmt='%.6f')  
    
if __name__ == '__main__':
    
    processedfiles = glob.glob('*_processed.txt')
    
    if len(processedfiles) != 0:
        os.system('rm *_processed.txt')
        
    detectors = glob.glob('*.txt')
    
    for d in detectors:
        efficiency(d)
        print(d, ' correctly processed')
        

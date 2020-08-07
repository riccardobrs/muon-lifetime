#python3 TxtToTex.py

import glob
import numpy as np
from io import *
from math import *
import os

                
def latexTxt(txtFiles):
    
    mV_dict = {}
    out_dict = {}
    outName = 'latex_{0}.txt'.format(txtFiles[0].split('_')[0])
    key_num = 0
    
    for f in txtFiles:
        mV_dict[f.split('_')[1].split('mV')[0]] = np.loadtxt(f)
        
    mV_dict = {k: val for k, val in sorted(mV_dict.items(), key=lambda item: float(item[0]))}
    
    for key in mV_dict.keys():
        for row in range(mV_dict[key].shape[0]):
            if not str(mV_dict[key][row][0]) in out_dict.keys():
                out_dict[str(mV_dict[key][row][0])] = '${0}$ & $U$ & $D$ & $T$ \\\\\n'.format(mV_dict[key][row][0])
            if key_num == 0:
                C = 'U'
            elif key_num == 1:
                C = 'D'    
            elif key_num == 2:
                C = 'T'
            T = float(mV_dict[key][row][2])
            D = float(mV_dict[key][row][3])
            eff = float(T)/D
            out_dict[str(mV_dict[key][row][0])] = out_dict[str(mV_dict[key][row][0])].replace(C, str(eff)+' \pm '+str(sqrt(eff*(1-eff)/D)))
        key_num += 1
            
    out_dict = {k: val for k, val in sorted(out_dict.items(), key=lambda item: float(item[0]))}
    
    with open(outName, 'a') as outfile:
        for key in out_dict.keys():
            outfile.write(out_dict[key].replace('$U$', '-').replace('$D$', '-').replace('$T$', '-'))
    
if __name__ == '__main__':
    
    caronte = glob.glob('Caronte*mV.txt')
    cerbero = glob.glob('Cerbero*mV.txt')
    minosse = glob.glob('Minosse*mV.txt')
    latexfiles = glob.glob('latex*.txt')
    
    if len(latexfiles) != 0:
        os.system('rm latex*.txt')
    
    latexTxt(caronte)
    latexTxt(cerbero)
    latexTxt(minosse)

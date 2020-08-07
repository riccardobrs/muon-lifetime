'''
This script is meant for execution of python scripts located in a parent root folder (that you can reach by running 'cd ..')

Actions performed:

    1) copy scripts(*) (mkTFile.py and mkMultigraph.py) and py-library (LabLib.py) in the folder where ExecuteAllScripts.py is run
    2) execute scripts(*) in a os.system shell
    3) remove scripts(*)

This script enables a better project management, avoiding to keep more than one version of the scripts in different folders

Important: it is needed that the folder containing data is called RateVsThreshold or RateVsBias

Folder management must be as follows:

    Offline_Lab_IV ---> only this must contain scripts(*) and py-library
        |
        |___ RateVsThreshold ---> This must contain data
        |
        |___ RateVsVoltage ---> This must contain data
        
How to run --->      python ExecuteAllScripts.py
'''

import os

if __name__ == '__main__':
    
    pylib = 'LabLib.py'
    scripts = ['mkTFile.py', 'mkMultiGraph.py']
    
    if not os.path.exists(pylib):
        os.system('cp ../{0} {0}'.format(pylib))

    if 'Threshold' in os.getcwd():
        RateVs = 'Threshold'
    elif 'Voltage' in os.getcwd():
        RateVs = 'Voltage'
    
    for script in scripts:
        if not os.path.exists(script):
            os.system('cp ../{0} {0}'.format(script))
        if script=='mkMultiGraph.py':
            os.system('python {0} --RateVs={1} --line=C'.format(script, RateVs))
        else:
            os.system('python {0} --RateVs={1}'.format(script, RateVs))
        os.remove(script)
    
    os.remove(pylib)
    os.remove(pylib+'c') #when scripts(*) are run, since they import LabLib.py, it is also created a file with name LabLib.pyc
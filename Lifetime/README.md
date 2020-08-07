# XML_parser.py

This script use ROOT framework, thus it must be run with Python 2. 
 
 
Libraries required: 
* numpy
* beautifulsoup4
* re
* argparse
* ROOT 

Given an input .xml file, _XML\_parser.py_ builds an output .root file structured in directories for each event, that store the acquired channels TGraph.


To use default argparse arguments values run with: 
 
 _python XML\_parser.py_ 
 
For any issue use the _help_ option: 
 
 _python XML\_parser.py -h_ 

Default argparse arguments values are:
* \-\-xml=./test
* \-\-rate=250.

thus the script will analyze the input _./test.xml_ and will produce the output _./test.root_. The digitizer sampling rate is considered to be equal to _250 MHz_ (default) 
 
Arguments can be modified using argparse options, for instance: 
 
 _python XML\_parser.py --xml=./FolderName/FileName1 --rate=244_ 
 
 _python XML\_parser.py -x=./FileName2_

 
# mkLifetimeHisto.py

This script uses ROOT framework, thus it must be run with Python 2 

Libraries required: 
* numpy
* argparse
* ROOT 

Given an input .root file (produced by _XML\_parser.py_ ) referred to a 2-channel Digitizer acquisition, _mkLifetimeHisto.py_ rejects all events with more than 2 pulses and computes the distance between the 2-pulses kept events, filling an histogram that is fitted by means of an exponential distribution. 
 
Outputs:
* lifetime.root
* lifetime.png

To use default argparse arguments values run with: 
 
 _python mkLifetimeHisto.py_ 
 
For any issue use the _help_ option: 
 
 _python mkLifetimeHisto.py -h_ 

Default argparse arguments values are:
* \-\-inputFile=./test
* \-\-threshold0=1200.
* \-\-threshold1=1200.
* \-\-rate=250.
* \-\-bins=50
* \-\-maxt=11.
* \-\-fmin=0.

Default fit method is chi square: to employ binned likelihood, you can use _-L_ option. 
 
Arguments can be modified using argparse options.

# show_events.py

This script plots some events. For _good_ events, derivatives are plotted too. Input .root file path is hardcoded into the script.
 
Run with 
 
 _python show\_events.py_

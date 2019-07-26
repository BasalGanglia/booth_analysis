import os
import pandas as pd
import json
import numpy as np
import datetime
import time

#  this returns a dataframe with two columns, first is ECG and second EDA, both sampled at 1000Hz
#  there is also bitalino_header attribute in the returned object containing timestamp in format
#  '11:16:52.678' and also a date object.. these have to be then converted to same time format as other
#  signals.

#  Psy date is bringing in the actual date as bitalino only has hours...

def parse_bitalino_directory(directory, psy_date):
    '''
    Takes as input the directory for the Bitalino files.
    Returns Pandas dataframe with 2 columns:
    1. time in seconds (since epoch)
    2. The trust gauge values (0-1024)    
    '''
    for root, dirs, files in os.walk(directory):        
        for filename in files:
            if ".txt" in filename:
                return parse_bitalino_file((directory + filename), psy_date)
            
def parse_bitalino_file(filename, psy_date):
 
    with open(filename) as f:
        stuff = f.readline()
        stuff = f.readline()
        print(" the interesting stuff is {0} ".format(stuff[1:]))
        tmp_header = json.loads(stuff[1:])
        
    
        #  lets generate a generic holder class for various stuff in the header and attach
        #  it to the pandas dataframe in the end.
        class bitalino_header(object) : pass
            
        device_id = next(iter(tmp_header))  #  There is only one key so this works...
        bitalino_header.header = tmp_header[device_id]
    
        #  We are specifically interested in the timestamp
        bitalino_header.timestamp = bitalino_header.header['time']
   

        stuff = pd.read_csv(filename, delimiter ='\t', comment=  '#', header= None, usecols=  [5, 6])
        stuff.bitalino_header = bitalino_header
        stuff.columns = ['ECG', 'EDA']
        
        stuff['Time'] = np.arange(len(stuff))
        
        bita_date =  datetime.datetime.strptime(bitalino_header.timestamp, '%H:%M:%S.%f')
        start_time = datetime.datetime(year = psy_date.year, month = psy_date.month, day = psy_date.day, hour = bita_date.hour, minute = bita_date.minute, second = bita_date.second,
                                       microsecond = bita_date.microsecond)

       #  Just a quick helper function to create timestamps row by row
        def my_funky(tehtime):
            return start_time + datetime.timedelta(milliseconds = float(tehtime))
        
        stuff['timestamp'] = stuff['Time'].map(my_funky)
  
        #  The bitalino samples at 1000Hz which is too much (the full datamatrix becomes gigabytes in size)
        #  downsample to 250 ms:
  
        _tmp = stuff.set_index(stuff['timestamp'])
        _tmp2 = _tmp.resample('4ms').mean()
        _tmp2 = _tmp2.drop(axis = 1, columns = 'Time')
        return _tmp2
    

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
            print("we atleast found filenames? " + filename)
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
   
      #  return bitalino_header
  
        stuff = pd.read_csv(filename, delimiter ='\t', comment=  '#', header= None, usecols=  [5, 6])
        stuff.bitalino_header = bitalino_header
        stuff.columns = ['ECG', 'EDA']
        
        stuff['Time'] = np.arange(len(stuff))
        
        #  Maybe there is a way to do this with apply but damn if i know how, so loop time it is
        
    #    for i in range (1000):  # range(len(stuff)):
     #       stuff.iloc[i, 2] = datetime.timedelta(milliseconds = float(stuff.iloc[i,2]) )
        
        # Above code is just way too slow...
        bita_date =  datetime.datetime.strptime(bitalino_header.timestamp, '%H:%M:%S.%f')
        start_time = datetime.datetime(year = psy_date.year, month = psy_date.month, day = psy_date.day, hour = bita_date.hour, minute = bita_date.minute, second = bita_date.second,
                                       microsecond = bita_date.microsecond)
        def my_funky(tehtime):
#            datetime.timedelta(milliseconds = float(tehtime))
            return start_time + datetime.timedelta(milliseconds = float(tehtime))
        
        stuff['timestamp'] = stuff['Time'].map(my_funky)
        #  The bitalino samples at 1000Hz which is too much (the full datamatrix becomes gigabytes in size)
        #  downsample to 250 ms:
     #   stuff = stuff.drop(axis = 1, columns = 'Time')
      #  return stuff
  #BELOW WORKS::      
        tmpduh = stuff.set_index(stuff['timestamp'])
        tmpduh2 = tmpduh.resample('4ms').mean()
        tmpduh2 = tmpduh2.drop(axis = 1, columns = 'Time')
        return tmpduh2
    
    
    
#  Below code does not work for whatever reason:
 #       stuff.index = stuff.set_index(pd.DatetimeIndex(stuff['timestamp']))
 #       stuff = stuff.resample('4ms').mean()
  #      stuff = stuff.drop(axis = 1, columns = 'Time')
    #    stuff.index = stuff.set_index('timestamp').resample('4ms')
 #       stuff['ECG'] = stuff.ECG.resample('4ms')
  #      stuff['EDA'] = stuff.EDa.resample('4ms')           
#        start_time =  datetime.datetime.strptime(bitalino_header.timestamp, '%H:%M:%S.%f')
#    return stuff
       

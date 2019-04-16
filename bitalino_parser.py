import os
import pandas as pd
import json

#  this returns a dataframe with two columns, first is ECG and second EDA, both sampled at 1000Hz
#  there is also bitalino_header attribute in the returned object containing timestamp in format
#  '11:16:52.678' and also a date object.. these have to be then converted to same time format as other
#  signals.


def parse_bitalino_directory(directory):
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
                return parse_bitalino_file((directory + filename))
            
def parse_bitalino_file(filename):
 
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
  
    return stuff

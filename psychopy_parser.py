import os
import pandas as pd
import json
import numpy as np
#  this returns a dataframe with two columns, first is ECG and second EDA, both sampled at 1000Hz
#  there is also bitalino_header attribute in the returned object containing timestamp in format
#  '11:16:52.678' and also a date object.. these have to be then converted to same time format as other
#  signals.


def parse_psychopy_directory(directory):
    '''
    Takes as input the directory for the Bitalino files.
    Returns Pandas dataframe with 2 columns:
    1. time in seconds (since epoch)
    2. The trust gauge values (0-1024)    
    '''
    for root, dirs, files in os.walk(directory):        
        for filename in files:
            print("we atleast found filenames? " + filename)
            if ".csv" in filename:
                return parse_psychopy_file((directory + filename))
            
def parse_psychopy_file(filename):
    
 
    stuff = pd.read_csv(filename, delimiter = ',')
 
    pdata = stuff[['startav', 'endav', 'startprim']].dropna(how = 'all')
#  Parsing these priming / avatar video orders gets pretty messy...
    avatar_data = stuff['avatar'].T
    priming_data = stuff['priming'].T
    
    avatar_data = avatar_data.dropna()
    priming_data = priming_data.dropna()
    #    avatar_data.dropna(inplace = True)
    #    priming_data.dropna(inplace = True)

    avatar_data = avatar_data.unique()
    priming_data = priming_data.unique()
# Im sure there has to be a more elegant way to do this but for now...  
    avatars = pd.DataFrame(data= {'avatar' : [avatar_data[0][-6:-4],  avatar_data[0][-6:-4],  avatar_data[1][-6:-4], avatar_data[1][-6:-4]]})
    primes= pd.DataFrame(data= {'prime' : [priming_data[0][-6:-4],  priming_data[0][-6:-4],  priming_data[1][-6:-4], priming_data[1][-6:-4]]})
    
    pdata['avatar'] = avatars.values
    pdata['primes'] = primes.values
    
    return pdata

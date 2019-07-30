""" File for parsing the opensignals output """
import os
import pandas as pd
import json
import numpy as np


def parse_psychopy_directory(directory):
    '''
    Takes as an argument the directory with PsychoPy files
    Goes through the directory, picks up the .csv file, processes it
    and returns relevant timing information.
    '''
    print("trying to access directory ", directory)
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if ".csv" in filename:
                return parse_psychopy_file((directory + filename))
            
def parse_psychopy_file(filename):
    """
    Parses out the time stamps when stimulus was being shown
    """
    stuff = pd.read_csv(filename, delimiter = ',')
 
    pdata = stuff[['startav', 'endav', 'startprim']].dropna(how = 'all')
#  Parsing these priming / avatar video orders gets pretty messy...
    avatar_data = stuff['avatar'].T
    priming_data = stuff['priming'].T
    
    avatar_data = avatar_data.dropna()
    priming_data = priming_data.dropna()
     
    avatar_data = avatar_data.unique()
    priming_data = priming_data.unique()
# Im sure there has to be a more elegant way to do this but for now...  
    avatars = pd.DataFrame(data= {'avatar' : [avatar_data[0][-6:-4],  avatar_data[0][-6:-4],  avatar_data[1][-6:-4], avatar_data[1][-6:-4]]})
    primes= pd.DataFrame(data= {'prime' : [priming_data[0][-6:-4],  priming_data[0][-6:-4],  priming_data[1][-6:-4], priming_data[1][-6:-4]]})
    
    pdata['avatar'] = avatars.values
    pdata['primes'] = primes.values
    
    return pdata

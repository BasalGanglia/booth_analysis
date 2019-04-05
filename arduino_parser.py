import os
import pandas as pd

def parse_arduino_directory(directory):
    '''
    Takes as input the directory for the Arduino file.
    Returns Pandas dataframe with 2 columns:
    1. time in seconds (since epoch)
    2. The trust gauge values (0-1024)
    we assume that the Arduino directry only has one file for each participant.
    
    '''
    for root, dirs, files in os.walk(directory):
        for filename in files:
            return parse_arduino_file((directory + filename))
            
def parse_arduino_file(filename):
    data = pd.read_csv(filename, header = None)
    data.columns = (['Time', 'Trust'])
    return data
    
import os
import pandas as pd

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
            if ".h5" in filename:
                return parse_bitalino_file((directory + filename))
            
def parse_bitalino_file(filename):
    data = pd.read_hdf(filename)
#    data.columns = (['Time', 'Trust'])
    return data

# reread = pd.read_hdf('./store.h5')
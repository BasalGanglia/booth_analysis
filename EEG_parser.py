import os
import scipy.io as sio  #  Scipy does not work with matlab v7.3 files...
# import h5py  #  not good either
import hdf5storage
import numpy as np
import datetime
import pandas as pd

def parse_eeg_directory(directory, psy_date):
    for root, dirs, files in os.walk(directory):        
        for filename in files:
            print("we atleast found filenames? " + filename)
            if ".mat" in filename:
                return parse_matlab_file((directory + filename), psy_date)

def parse_matlab_file(filename, psy_date):
    mat_contents = hdf5storage.loadmat(filename)
    #  Mat_contents is now a dictionary with one key, y, that contains a (15,m) numpy array
    #  the final six rows contain the timestamp: 

  
    data = mat_contents['y']
    timerows = data[-6:, :]
 
    mat_df = pd.DataFrame(timerows)
    data = data[:-6, :]
    timerows = timerows.T
    data = data.T
    eeg_data = np.concatenate((timerows, data), axis = 1)
    eeg_data = pd.DataFrame(eeg_data, columns= ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'SfromStart', 'Ch1', 'Ch2', 'Ch3', 'Ch4', 'Ch5', 'Ch6', 'Ch7', 'Ch8'])
    eeg_date = datetime.datetime(int(eeg_data.iloc[0, 0]), int(eeg_data.iloc[0, 1]) , int(eeg_data.iloc[0, 2]), int(eeg_data.iloc[0, 3]), int(eeg_data.iloc[0, 4]), int(eeg_data.iloc[0, 5]))
    
    start_time = datetime.datetime(year = psy_date.year, month = psy_date.month, day = psy_date.day, hour = eeg_date.hour, minute = eeg_date.minute, second = eeg_date.second,
                                   microsecond = eeg_date.microsecond)
    
    def my_funky(tehtime):
        return start_time + datetime.timedelta(seconds = float(tehtime[6] ))

    eeg_data["timestamp"] = eeg_data.apply(my_funky, axis = 1)

    return eeg_data
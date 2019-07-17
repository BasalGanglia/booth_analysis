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

   # mat_df = pd.Dataframe(mat_contents)
    data = mat_contents['y']
    timerows = data[-6:, :]
    print("first row is ", timerows[:, 0])

    mat_df = pd.DataFrame(timerows)
#    times= mat_df.apply(lambda x: datetime.datetime(int(x[0]) , int(x[1] ), int(x[ 2] ), int(x[3] ), int(x[4]), int(x[ 5])))
    data = data[:-6, :]
    timerows = timerows.T
    data = data.T
    eeg_data = np.concatenate((timerows, data), axis = 1)
    eeg_data = pd.DataFrame(eeg_data, columns= ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'SfromStart', 'Ch1', 'Ch2', 'Ch3', 'Ch4', 'Ch5', 'Ch6', 'Ch7', 'Ch8'])
    eeg_date = datetime.datetime(int(eeg_data.iloc[0, 0]), int(eeg_data.iloc[0, 1]) , int(eeg_data.iloc[0, 2]), int(eeg_data.iloc[0, 3]), int(eeg_data.iloc[0, 4]), int(eeg_data.iloc[0, 5]))
    
    start_time = datetime.datetime(year = psy_date.year, month = psy_date.month, day = psy_date.day, hour = eeg_date.hour, minute = eeg_date.minute, second = eeg_date.second,
                                   microsecond = eeg_date.microsecond)
    
    def my_funky(tehtime):
#            datetime.timedelta(milliseconds = float(tehtime))
        return start_time + datetime.timedelta(seconds = float(tehtime[6] ))
    #    return datetime.datetime(year = int(tehtime.iloc[0]), month = int(tehtime.iloc[1]), day = int(tehtime.iloc[2]), hour = int(tehtime.iloc[3]), minute = int(tehtime.iloc[4]),
     #                            second = int(tehtime.iloc[5]), microsecond = int(tehtime.iloc[6]))   
    
 #   EEG = pd.DataFrame(data)
  #  stuff['timestamp'] = stuff['Time'].map(my_funky)
     
    eeg_data["timestamp"] = eeg_data.apply(my_funky, axis = 1)
    # as the arduino outputs seconds since epochs we have to use that as the common time format
    
   # with h5py.File(filename, 'r') as f:
   #     mat_contents = f.keys()
  #  return times
#    return EEG
    return eeg_data
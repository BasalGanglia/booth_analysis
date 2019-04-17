import os
import scipy.io as sio  #  Scipy does not work with matlab v7.3 files...
import h5py  #  not good either
import hdf5storage
 



def parse_eeg_directory(directory):
    for root, dirs, files in os.walk(directory):        
        for filename in files:
            print("we atleast found filenames? " + filename)
            if ".mat" in filename:
                return parse_matlab_file((directory + filename))

def parse_matlab_file(filename):
    mat_contents = hdf5storage.loadmat(filename)
    #  Mat_contents is now a dictionary with one key, y, that contains a (15,m) numpy array
    #  the final six rows contain the timestamp: 

    
    data = mat_contents['y']
    timerows = data[-6:, :]
    timerows = timerows.T
    
    # as the arduino outputs seconds since epochs we have to use that as the common time format
    
   # with h5py.File(filename, 'r') as f:
   #     mat_contents = f.keys()
    
    return mat_contents
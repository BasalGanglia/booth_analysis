import datetime
import pandas as pd
import os
DATA_ROOT_DIR = "C:\\Users\\ilkka\\data\\Booth\\experiment\\"

EXAMPLE_DIR = DATA_ROOT_DIR + "CSPM2"
ARDUINO_DIR = EXAMPLE_DIR + "\\arduino\\"
BITALINO_DIR = EXAMPLE_DIR + "\\bitalino\\"
EEG_DIR = EXAMPLE_DIR + "\\eeg\\"
PSYCHOPY_DIR = EXAMPLE_DIR + "\\psychopy\\"
# The following silly snippet might be needed when running
#  stuff in Wing IDE python shell which seems not to default
#  into the project working directory

#import os
#os.chdir("C:\\Users\\ilkka\\code\\booth_analysis")


import arduino_parser
import bitalino_parser
import opensignals_reader
import EEG_parser
import psychopy_parser

import imp

def parse_user(subjectid):

    #  Ok, following could maybe be done more elegantly
    DATA_ROOT_DIR = "C:\\Users\\ilkka\\data\\Booth\\experiment\\I_b1w2\\data_sorted_by_participant\\"	
    EXAMPLE_DIR = DATA_ROOT_DIR + subjectid
    ARDUINO_DIR = EXAMPLE_DIR + "\\arduino\\"
    BITALINO_DIR = EXAMPLE_DIR + "\\bitalino\\"
    EEG_DIR = EXAMPLE_DIR + "\\eeg\\"
    PSYCHOPY_DIR = EXAMPLE_DIR + "\\psychopy\\"    
    print("The psychopydir is", PSYCHOPY_DIR)
    imp.reload(psychopy_parser)
    psychopy_data = psychopy_parser.parse_psychopy_directory(PSYCHOPY_DIR)
    
    # parsing date from psychopy as it is not in all the individual datafiles:
    psy_date = datetime.datetime.strptime(psychopy_data.iloc[0, 0], '%Y-%m-%d %H:%M:%S.%f')
    
    # Parse the EEG DATA:
    imp.reload(EEG_parser)
    eeg_data = EEG_parser.parse_eeg_directory(EEG_DIR, psy_date)
    
    #  Parse the Trust feedback recorded with Arduino:
    imp.reload(arduino_parser)
    arduino_data = arduino_parser.parse_arduino_directory(ARDUINO_DIR, psy_date)
    
    #  Parse out ECG and EDA recorded with Bitalino:
    imp.reload(bitalino_parser)
    bitalino_data = bitalino_parser.parse_bitalino_directory(BITALINO_DIR, psy_date)
    
    # Merge the data from EEG, Bitalino (EDA/ECG) and Arduino (trust)
    test_merge = pd.merge(eeg_data, bitalino_data, how = 'left', on= 'timestamp')
    test_merge2 = pd.merge(test_merge, arduino_data, how= 'left', on = 'timestamp')
    
    #  The data was sampled at different sampling rates. Linearly interpolate data for the slower sampling rate
    #  signals: 
    final_data = test_merge2.interpolate()
    #  Drop useless columns
    final_data = final_data.drop(columns = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'SfromStart', 'Time'])
    final_data['Subjectid'] = subjectid
    return final_data



if __name__ == '__main__':

    datadir = "C:\\Users\\ilkka\\data\\Booth\\experiment\\I_b1w2\\data_sorted_by_participant"
#using the silly i because enumerate complained about syntax error for reason i did not have time to investigate
    i = 1
    for filename in os.listdir(datadir):
        print("We found this file: ", filename , " which is the ", i)
        if i == 1:
            data = parse_user(filename)
        else:
            data = pd.concat([data, parse_user(filename)])
        #  enumerate did not work for whatever reason
        i = i + 1
     #   if i > 2:            
       #     break
        
        #if filename.endswith(".txt"):
            #f = open(filename)
            #lines = f.read()
            #print (lines[10])
            #continue
        #else:
        #continue      
  #  one_user = parse_user("CSPM2")
    

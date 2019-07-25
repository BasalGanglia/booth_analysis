import datetime
from datetime import timedelta
import pandas as pd
import os
DATA_ROOT_DIR = "C:\\Users\\ilkka\\data\\Booth\\experiment\\"
LABELS_FILE = DATA_ROOT_DIR + 'Empathy_labels.csv'

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

#  Quick helper method to change the data types from float64 to float32 to save some space
def change_floats(df, column_list):
    df[column_list] = df[column_list].apply(pd.to_numeric, downcast = 'float')
    return df

def parse_user(subjectid, datadir):

    #  Ok, following could maybe be done more elegantly
    #   DATA_ROOT_DIR = "C:\\Users\\ilkka\\data\\Booth\\experiment\\I_b1w2\\data_sorted_by_participant\\"
    DATA_ROOT_DIR = datadir
    
    EXAMPLE_DIR = DATA_ROOT_DIR + subjectid
#    EXAMPLE_DIR = "C:\\Users\\ilkka\\data\\Booth\\experiment\\II_b2w1\\data_sorted_by_participant\\B0HBS"
    ARDUINO_DIR = EXAMPLE_DIR + "\\arduino\\"
    BITALINO_DIR = EXAMPLE_DIR + "\\bitalino\\"
    EEG_DIR = EXAMPLE_DIR + "\\eeg\\"
    PSYCHOPY_DIR = EXAMPLE_DIR + "\\psychopy\\"    
    print("The psychopydir is", PSYCHOPY_DIR)
    
    labels = pd.read_csv(LABELS_FILE, sep = ';')
    
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
    finaldata = test_merge2.interpolate()
    #  Drop useless columns
    finaldata = finaldata.drop(columns = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'SfromStart', 'Time'])
    finaldata['Subjectid'] = subjectid
    final_data = finaldata.set_index('timestamp')
    final_data = change_floats(final_data, ['Ch1', 'Ch2', 'Ch3', 'Ch4', 'Ch5', 'Ch6', 'Ch7', 'Ch8', 'ECG', 'EDA'])
    #  this code is pretty ugly due to the different timestamp formats these pandas methods require..
    trust_start_1 = datetime.datetime.strptime(psychopy_data['startav'].iloc[1], '%Y-%m-%d %H:%M:%S.%f')
    trust_start_2 = datetime.datetime.strptime(psychopy_data['startav'].iloc[3], '%Y-%m-%d %H:%M:%S.%f')
    trust_end_1 = datetime.datetime.strptime(psychopy_data['endav'].iloc[1], '%Y-%m-%d %H:%M:%S.%f')
    trust_end_2 = datetime.datetime.strptime(psychopy_data['endav'].iloc[3], '%Y-%m-%d %H:%M:%S.%f')
    
    trust_data = final_data.between_time(trust_start_1.strftime("%H:%M:%S"),trust_end_1.strftime("%H:%M:%S"))
    trust_data = pd.concat([trust_data, final_data.between_time(trust_start_2.strftime("%H:%M:%S"),trust_end_2.strftime("%H:%M:%S"))])


    # Parsing out the parts with different amount of empathy:
  
    for idxi, label in labels.iterrows():
        
  
        start_t = datetime.datetime.strptime(label.starting_time, '%M:%S')
        end_t = datetime.datetime.strptime(label.ending_time, '%M:%S')
        
        start_delta = timedelta(minutes = start_t.minute, seconds = start_t.second)
        end_delta = timedelta(minutes = end_t.minute, seconds = end_t.second)    
        
        neutral_slice = final_data.between_time((final_data.index[0] + start_delta).time(), (final_data.index[0] + end_delta).time())
        neutral_slice['empathy_level'] = label.empathy_level        
        
        if idxi == 0:
            neutral_slices = neutral_slice
        else:
            neutral_slices = pd.concat([neutral_slices, neutral_slice])
        
        #start_t = datetime.datetime.strptime(labels.iloc[1].starting_time, '%M:%S')
        #end_t = datetime.datetime.strptime(labels.iloc[1].ending_time, '%M:%S')
        
        #start_delta = timedelta(minutes = start_t.minute, seconds = start_t.second)
        #end_delta = timedelta(minutes = end_t.minute, seconds = end_t.second)    
    
        #neutral_slice = final_data.between_time((final_data.index[0] + start_delta).time(), (final_data.index[0] + end_delta).time())
        #neutral_slice['empathy_level'] = labels.iloc[1].empathy_level
# test_sub.between_time(test_sub.index[0].time(), (test_sub.index[0] + delta).time())

   # what  psychopy_data looks like
        #startav                       endav  ...   avatar primes
    #1   2018-11-12 12:35:16.594000  2018-11-12 12:40:16.971000  ...       w1     p1
    #44  2018-11-12 12:51:33.194000  2018-11-12 12:56:33.700000  ...       w1     p1
    #45  2018-11-12 13:05:55.843000  2018-11-12 13:10:56.224000  ...       b2     p2
    #88  2018-11-12 13:15:52.631000  2018-11-12 13:20:53.029000  ...       b2     p2   
    #  HERE WE MUST EXTRACT THE ACTUAL FEATURES INSTEAD OF RAW DATA:
    
    
    
    return final_data, psychopy_data, trust_data, neutral_slice




if __name__ == '__main__':

 #   datadir = "C:\\Users\\ilkka\\data\\Booth\\experiment\\I_b1w2\\data_sorted_by_participant"
    datadir = "C:\\Users\\ilkka\\data\\Booth\\experiment\\II_b2w1\\data_sorted_by_participant\\"

#using the silly i because enumerate complained about syntax error for reason i did not have time to investigate
    i = 1

    
    for filename in os.listdir(datadir):
        print("We found this file: ", filename , " which is the ", i)
   
 #       if filename != "W0PIK":
  #         continue;
       
   #     if filename != "MDPQ4":    
#            continue;
        if i == 1:
            all_data, all_timestamps, all_trust, all_empathy = parse_user(filename, datadir)
        else:
            data2, psyd2, trust_dat2, empathy2 = parse_user(filename, datadir)
       
            all_data = pd.concat([all_data, data2])
            all_timestamps = pd.concat([all_timestamps, psyd2])
            all_trust = pd.concat([all_trust, trust_dat2])
            all_empathy = pd.concat([all_empathy, empathy2])
            #           data = pd.concat([data, parse_user(filename, datadir)])
        #  enumerate did not work for whatever reason
        i = i + 1
   #     if i > 1:
    #        break
        
        #if filename.endswith(".txt"):
            #f = open(filename)
            #lines = f.read()
            #print (lines[10])
            #continue
        #else:
        #continue      
  #  one_user = parse_user("CSPM2")
  

import datetime

DATA_ROOT_DIR = "C:\\Users\\ilkka\\data\\Booth\\experiment\\"

EXAMPLE_DIR = DATA_ROOT_DIR + "example"
ARDUINO_DIR = EXAMPLE_DIR + "\\arduino\\"
BITALINO_DIR = EXAMPLE_DIR + "\\bitalino\\"
EEG_DIR = EXAMPLE_DIR + "\\eeg\\"
PSYCHOPY_DIR = EXAMPLE_DIR + "\\psychopy\\"
# The following silly snippet might be needed when running
#  stuff in Wing IDE python shell which seems not to default
#  into the project working directory
#import os
#os.chdir("C:\\Users\\ilkka\\code\\booth_analysis")

# import h5py
# from arduino_parser import parse_arduino_file

import arduino_parser
import bitalino_parser
import opensignals_reader
import EEG_parser
import psychopy_parser

import imp
# imp.reload(arduino_parser)
# imp.reload(bitalino_parser)
imp.reload(psychopy_parser)
psychopy_data = psychopy_parser.parse_psychopy_directory(PSYCHOPY_DIR)

# parsing datime from psychopy:
psy_date = datetime.datetime.strptime(psychopy_data.iloc[0, 0], '%Y-%m-%d %H:%M:%S.%f')

imp.reload(EEG_parser)
eeg_data = EEG_parser.parse_eeg_directory(EEG_DIR, psy_date)
#muf2 = EEG_parser.parse_eeg_directory(EEG_DIR)

## puf = bitalino_parser.parse_bitalino_directory(BITALINO_DIR)
imp.reload(arduino_parser)
arduino_data = arduino_parser.parse_arduino_directory(ARDUINO_DIR, psy_date)
## bitalino_data2 = bitalino_parser.parse_bitalino_directory(BITALINO_DIR)
## bitalino_data = bitalino_parser.parse_bitalino_directory(BITALINO_DIR)

imp.reload(bitalino_parser)
bitalino_data = bitalino_parser.parse_bitalino_directory(BITALINO_DIR, psy_date)

# bitalino_data2 = bitalino_data.apply(datetime)

bit_date = datetime.datetime.strptime(bitalino_data.bitalino_header.timestamp, '%H:%M:%S.%f')
bit_date = bit_date.replace(year = psy_date.year)
bit_date = bit_date.replace(month = psy_date.month)
bit_date = bit_date.replace(day = psy_date.day)
arduino_time = datetime.datetime.utcfromtimestamp(arduino_data['Time'].iloc[0]).strftime('%Y-%m-%d %H:%M:%S')
arduino_date = datetime.datetime.strptime(arduino_time, '%Y-%m-%d %H:%M:%S')

# eeg_date = datetime.datetime(int(eeg_data.iloc[0, 0]), int(eeg_data.iloc[1, 0]) , int(eeg_data.iloc[2, 0]), int(eeg_data.iloc[3, 0]), int(eeg_data.iloc[4, 0]), int(eeg_data.iloc[5, 0]))
#  Arduino logs are really screwed up... for soem reason the non-changing values are logged million times
#  something like this : len(arduino_data['Time'].unique())
#psychopy_data.columns = ['time', 'wat', 'data']
#psychopy_data =psychopy_data[~psychopy_data.data.str.contains('blendMode')]
#psychopy_data =psychopy_data[~psychopy_data.data.str.contains('MovieStim2')]
#psychopy_data =psychopy_data[~psychopy_data.data.str.contains('MovieStim2')]
# import pandas as pd

# psychopy_data.to_csv("remainders.csv")



# type(bitalino_data2.head_information)



#if __name__ == '__main__':
    #main()
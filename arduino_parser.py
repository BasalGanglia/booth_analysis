import os
import pandas as pd
import datetime
#  data is in format : 1541503443,1023
def parse_arduino_directory(directory, psy_date):
    '''
    Takes as input the directory for the Arduino file.
    Returns Pandas dataframe with 2 columns:
    1. time in seconds (since epoch)
    2. The trust gauge values (0-1024)
    we assume that the Arduino directry only has one file for each participant.
    
    '''
    for root, dirs, files in os.walk(directory):
        for filename in files:
            return parse_arduino_file((directory + filename), psy_date)
            
def parse_arduino_file(filename, psy_date):
    data = pd.read_csv(filename, header = None)
    data.columns = (['Time', 'Trust'])
    
  #  data['Time']= datetime.datetime.utcfromtimestamp(data['Time']).strftime('%Y-%m-%d %H:%M:%S')
 #   arduino_date = datetime.datetime.strptime(arduino_time, '%Y-%m-%d %H:%M:%S')
  
    # Above code is just way too slow...
 
#    ard_date =  datetime.datetime.strptime(bitalino_header.timestamp, '%H:%M:%S.%f')
 #   start_time = datetime.datetime(year = psy_date.year, month = psy_date.month, day = psy_date.day, hour = bita_date.hour, minute = bita_date.minute, second = bita_date.second,
#                                   microsecond = bita_date.microsecond)
    def my_funky(tehtime):
        #            datetime.timedelta(milliseconds = float(tehtime))
        return datetime.datetime.utcfromtimestamp(tehtime)
    
    data['timestamp'] = data['Time'].map(my_funky)    
    return data

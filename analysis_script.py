DATA_ROOT_DIR = "C:\\Users\\ilkka\\data\\Booth\\experiment\\"

EXAMPLE_DIR = DATA_ROOT_DIR + "example"
ARDUINO_DIR = EXAMPLE_DIR + "\\arduino\\"
BITALINO_DIR = EXAMPLE_DIR + "\\bitalino\\"

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

import imp
imp.reload(arduino_parser)
imp.reload(bitalino_parser)
# puf = bitalino_parser.parse_bitalino_directory(BITALINO_DIR)

# arduino_data = arduino_parser.parse_arduino_directory(ARDUINO_DIR)
# bitalino_data2 = bitalino_parser.parse_bitalino_directory(BITALINO_DIR)
# bitalino_data = bitalino_parser.parse_bitalino_directory(BITALINO_DIR)
#  Following code for plotting bitalino stuff
#  import matplotlib.pyplot as plt
#  plt.plot(puf.iloc[1:100, 1])


# type(bitalino_data2.head_information)



#if __name__ == '__main__':
    #main()
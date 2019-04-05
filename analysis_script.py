DATA_ROOT_DIR = "C:\\Users\\ilkka\\data\\Booth\\experiment\\"

EXAMPLE_DIR = DATA_ROOT_DIR + "example"
ARDUINO_DIR = EXAMPLE_DIR + "\\arduino\\"
BITALINO_DIR = EXAMPLE_DIR + "\\bitalino\\"

# The following silly snippet might be needed when running
#  stuff in Wing IDE python shell which seems not to default
#  into the project working directory
#import os
#os.chdir("C:\\Users\\ilkka\\code\\booth_analysis")

import h5py
# from arduino_parser import parse_arduino_file

import arduino_parser
import bitalino_parser
import imp
imp.reload(arduino_parser)
imp.reload(bitalino_parser)
# arduino_data = arduino_parser.parse_arduino_directory(ARDUINO_DIR)
bitalino_data = bitalino_parser.parse_bitalino_directory(BITALINO_DIR)

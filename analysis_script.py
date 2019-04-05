DATA_ROOT_DIR = "C:\\Users\\ilkka\\data\\Booth\\experiment\\"

EXAMPLE_DIR = DATA_ROOT_DIR + "example"
ARDUINO_DIR = EXAMPLE_DIR + "\\arduino\\"

# The following silly snippet might be needed when running
#  stuff in Wing IDE python shell which seems not to default
#  into the project working directory
#import os
#os.chdir("C:\\Users\\ilkka\\code\\booth_analysis")

import h5py
# from arduino_parser import parse_arduino_file

import arduino_parser
import imp
arduino_parser.parse_arduino_file(ARDUINO_DIR)
imp.reload(arduino_parser)

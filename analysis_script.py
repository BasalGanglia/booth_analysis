DATA_ROOT_DIR = "C:\\Users\\ilkka\\data\\Booth\\experiment\\"

EXAMPLE_DIR = DATA_ROOT_DIR + "example"

# The following silly snippet might be needed when running
#  stuff in Wing IDE python shell which seems not to default
#  into the project working directory
#import os
#os.chdir("C:\\Users\\ilkka\\code\\booth_analysis")

import h5py
# from arduino_parser import parse_arduino_file

import arduino_parser

arduino_parser.parse_arduino_file(EXAMPLE_DIR)


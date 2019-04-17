# TODO:
- Matlab script that goes through EEG data from all participants and parses it out in suitable format
- A script that runs the python parsers on all the test subjects and store the data in a big dataframe
- decide on common timeformat
- check the interesting timings from Angela
- get the start times from psychopy files
- pyEEG
- bandpass extraction

# booth_analysis

## General Problems
The directory names are not uniformly named.. for example there might be "bitolino" instead of "bitalino"

## Bitalino
data in HD5F format. Trying to use pandas to import the data and get following error:
"ImportError: HDFStore requires PyTables, "No module named tables" problem importing"
googling solves the issue (conda install pytables)
next error:
No dataset in HDF5 file.
pandas read_hdf() does not seem to work with this data, have to use lower level HDFStore() which
returns something...


XBh6MeuxDfzA6Mu

"""
This script contain just various code snippets I tried out 
"""

# test_sub = all_data[all_data['Subjectid'] == 'YY40E']
# import pickle
import pandas as pd
import mne
test_sub = pd.read_pickle("test2.pkl")
eegchannels = test_sub.iloc[:, 0:8]
ch_names = list(eegchannels.columns)
sfreq = 250
ch_types = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']
info = mne.create_info(ch_names, sfreq, ch_types = ch_types)

# Finally, create the Raw object
raw = mne.io.RawArray(eegchannels.T, info)

# Plot it!
scalings = 'auto'
# raw.plot(scalings = scalings)

#start, stop = raw.time_as_index([1000, 1150])  # 100 s to 115 s data segment
#data, times = raw[:, start:stop]
#print(data.shape)
#print(times.shape)
#data, times = raw[2:20:3, start:stop]  # access underlying data
#data.plot()

#  trying to filter the data:


fmin, fmax = 1, 100 # look at frequencies between 2 and 300Hz
n_fft = 2048  # the FFT size (n_fft). Ideally a power of 2


f, (ax1, ax2) = plt.subplots(2, 1, sharey=False)
# 
#
raw2 = raw.copy()
raw2.filter(8., 12., method= 'iir')
raw2.plot_psd(area_mode='range', tmax=10.0, picks=['Ch1'], ax = ax1, n_fft = n_fft)

raw2 = raw.copy()
# raw2.filter(1., 30., method= 'iir')
raw2.filter(8, 12, fir_design='firwin')
raw2.plot_psd(area_mode='range', tmax=100.0, picks=['Ch1'], ax = ax2,  n_fft = n_fft)

selection = mne.read_selection('Ch1')
picks = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, stim=False)
raw.plot_psd(area_mode='range', tmax=10.0, picks=picks)

raw2 = raw
raw2.crop(200, 300).load_data()
scalings = 'auto'
raw2.plot(scalings = scalings)
rawbackup = raw
raw.filter(7., 30., method= 'iir')
raw.filter(1, 30, fir_design='firwin')

# Using FFT to extract the values:

test_sub = pd.read_pickle("test2.pkl")
eegchannels = test_sub.iloc[:, 0:8]
ch_names = list(eegchannels.columns)
sfreq = 250
ch_types = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']
info = mne.create_info(ch_names, sfreq, ch_types = ch_types)

# Finally, create the Raw object
raw = mne.io.RawArray(eegchannels.T, info)



#   USE THE MULTITAPER that comes with mne
test_sub = pd.read_pickle("test2.pkl")
eegchannels = test_sub.iloc[:, 0:8]
ch_names = list(eegchannels.columns)
sfreq = 250
ch_types = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']
info = mne.create_info(ch_names, sfreq, ch_types = ch_types)

# Finally, create the Raw object
from mne.time_frequency import psd_multitaper


raw = mne.io.RawArray(eegchannels.T, info)
tmin, tmax = 0, 60  # use the first 60s of data
f, ax = plt.subplots()
psds, freqs = psd_multitaper(raw, low_bias=True, tmin=tmin, tmax=tmax,
                             fmin=fmin, fmax=fmax, proj=True, picks=['all'],
                             n_jobs=1)
psds = 10 * np.log10(psds)
psds_mean = psds.mean(0)
psds_std = psds.std(0)



ax.plot(freqs, psds_mean, color='k')
ax.fill_between(freqs, psds_mean - psds_std, psds_mean + psds_std,
                color='k', alpha=.5)
ax.set(title='Multitaper PSD', xlabel='Frequency',
       ylabel='Power Spectral Density (dB)')
plt.show()

#  Extract eeg bands (modifying https://dsp.stackexchange.com/questions/45345/how-to-correctly-compute-the-eeg-frequency-bands-with-python) :

fft_freq = np.fft.rfftfreq((60 *250), 1.0 / sfreq)


# Define EEG bands
eeg_bands = {'Delta': (0, 4),
             'Theta': (4, 8),
             'Alpha': (8, 12),
             'Beta': (12, 30),
             'Gamma': (30, 45),
             'artifact': (49, 51),
             'dummy': (52, 54)}

# Take the mean of the fft amplitude for each EEG band
eeg_band_fft = dict()
for band in eeg_bands:  
    freq_ix = np.where((fft_freq >= eeg_bands[band][0]) & 
                       (fft_freq <= eeg_bands[band][1]))[0]
    eeg_band_fft[band] = np.mean(psds_mean[freq_ix])

# Plot the data (using pandas here cause it's easy)
import pandas as pd
df = pd.DataFrame(columns=['band', 'val'])
df['band'] = eeg_bands.keys()
df['val'] = [eeg_band_fft[band] for band in eeg_bands]
ax = df.plot.bar(x='band', y='val', legend=False)
ax.set_xlabel("EEG band")
ax.set_ylabel("Mean band Amplitude")



#  Wide to long ...

import numpy as np
import pandas as pd



#  There don't seem to be ready made way to go from wide to long this way, so
#  I suppose it have to do it manually.. there probably is some much more elegant
#  way to do it but what the heck, for loop time!
#  edit: this merge nonsense is ridiculous... is there really no working way in pandas
#  to concatenate columns..
for i in range(0, 8):  
    one_row_df = data.iloc[[i], :]
    one_row_df.columns = one_row_df.columns + str(i)
    one_row_df['merger'] = 1
    if i == 0:        
        new_df = one_row_df.copy( ) 
    else:
        new_df = pd.merge( one_row_df, new_df, how = 'outer', on = 'merger')
    #    new_df = pd.concat([new_df, one_row_df], ignore_index= True, axis= 1)
    new_df.drop('merger', inplace = True, axis = 1)
    return new_df

def widen_features(df):
    for i in range(0, 8):  
        one_row_df = df.iloc[[i], :].copy()
        one_row_df.columns = one_row_df.columns + str(i)
        one_row_df['merger'] = 1
        if i == 0:        
            new_df = one_row_df.copy( ) 
        else:
            new_df = pd.merge( one_row_df, new_df, how = 'outer', on = 'merger')
        #    new_df = pd.concat([new_df, one_row_df], ignore_index= True, axis= 1)
        
    new_df.drop('merger', inplace = True, axis = 1)
        
    return new_df
    
import pandas as pd
import mne
import numpy as np
from mne.time_frequency import psd_multitaper


def Analyze_EEG(df):
    # test_sub = pd.read_pickle("test2.pkl")
    test_sub = df
    eegchannels = test_sub.iloc[:, 0:8]
    ch_names = list(eegchannels.columns)
    sfreq = 250
    ch_types = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']
    info = mne.create_info(ch_names, sfreq, ch_types = ch_types)
    
    # Create the Raw object
    
    raw = mne.io.RawArray(eegchannels.T, info)
#    tmin, tmax = 0, 60  # use the first 60s of data
    tmin, tmax = 0,  len(raw.get_data('Ch1')[0])
    #  Data was already notch filtered during recording at around 50Hz.
    
    #  sidenote: the raw object can be accessed as so:
    #    len(raw.get_data('Ch1')[0])
    #  returns 770206
    
    #  psd_multitaper returns power spectral densities in psd (in this case
    #  in shape (n_channels, n_freqs). The freqs contains information at
    #  which frequency we had this power. The frequencies are spread between
    #  the values defined below:
    fmin, fmax = 1, 100
    
    psds, freqs = psd_multitaper(raw, low_bias=True, tmin=tmin, tmax=tmax,
                                 fmin=fmin, fmax=fmax, proj=True, picks=['all'],
                                 n_jobs=1)
    psds = 10 * np.log10(psds)
    
    psds_mean = psds.mean(0)
    psds_std= psds.std(0)
    
    #  To convert the data into sensible band powers, we need to convert to Hz and extract the bands
    # The Hz conversion is data_length divided by (1/sampling freq)    
    fft_freq = np.fft.rfftfreq((len(raw.get_data('Ch1')[0]) ), 1.0 / sfreq)
#    fft_freq = np.fft.rfftfreq((60 *sfreq ), 1.0 / sfreq)    
    
    # Define EEG bands
    eeg_bands = {'Delta': (0, 4),
                 'Theta': (4, 8),
                 'Alpha': (8, 12),
                 'Beta': (12, 30),
                 'Gamma_low': (30, 45),
                 'Gamma_high': (55, 80)}
    
    eeg_band_fft = dict()
    for band in eeg_bands:  
        freq_ix = np.where((fft_freq >= eeg_bands[band][0]) & 
                           (fft_freq <= eeg_bands[band][1]))[0]
        eeg_band_fft[band] = np.mean(psds[:, freq_ix], axis = 1)

    for band in eeg_bands:  
        freq_ix = np.where((fft_freq >= eeg_bands[band][0]) & 
                           (fft_freq <= eeg_bands[band][1]))[0]
        eeg_band_fft[band + '_std'] = np.std(psds[:, freq_ix], axis = 1)
    
    #  create a Pandas DataFrame, and normalize the values for each participant
    eeg_df = pd.DataFrame.from_dict(eeg_band_fft)

    #  Lets normalize each participant: we are only interested in the relative differences between
    # electrodes
    
    overall_power_mean = np.mean(np.mean(eeg_df.iloc[:, 0:6]) )
    eeg_df.iloc[:, 0:6] = eeg_df.iloc[:, 0:6] / overall_power_mean 
    overall_std_mean = np.mean(np.mean(eeg_df.iloc[:, 6:]) )
    eeg_df.iloc[:, 6:] = eeg_df.iloc[:, 6:] / overall_std_mean 
    return eeg_df
# egg_df = Analyze_EEG(pd.DataFrame())
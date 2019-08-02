import neurokit as nk
import pandas as pd
import numpy as np
import seaborn as sns
import imp
imp.reload(nk)

def extract_peripheral_features(df): 
    bio = nk.bio_process(ecg= df['ECG'], eda= df['EDA'], sampling_rate= 250)

        
    features = {}
    if (('HF' in bio['ECG']['HRV']) == False):
        return features
    features['CVSD'] = bio['ECG']['HRV']['CVSD']
    features['HF'] = bio['ECG']['HRV']['HF']
    features['HF/P'] = bio['ECG']['HRV']['HF/P']
    features['LF'] = bio['ECG']['HRV']['LF']
    features['LF/HF'] = bio['ECG']['HRV']['LF/HF']
    features['LF/P'] = bio['ECG']['HRV']['LF/P']
    features['LF/n'] = bio['ECG']['HRV']['LFn']
    features['RMSSD'] = bio['ECG']['HRV']['RMSSD']
    features['CVSD'] = bio['ECG']['HRV']['CVSD']
    features['HF'] = bio['ECG']['HRV']['HF']
    features['CVSD'] = bio['ECG']['HRV']['CVSD']
    features['HF'] = bio['ECG']['HRV']['HF']
    features['EDA_mean_amp'] = np.mean(bio['EDA']['SCR_Peaks_Amplitudes'])
#  Divide by length so longer and shorter segments are treated equally (5 peaks in 10 seconds is more than
#  5 peaks in 30 seconds
    features['EDA_num_peaks'] = len(bio['EDA']['SCR_Peaks_Amplitudes']) / len(df)

    return features
    



    
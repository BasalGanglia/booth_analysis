import neurokit as nk
import pandas as pd
import numpy as np
import seaborn as sns
#test_sub = pd.read_pickle('test_sub.pkl')
# short_sub = test_sub.iloc[0:100000, :]
#test_emp = test_sub.iloc[100000:107500, :]

#bio = nk.bio_process(ecg = test_emp['ECG'], eda= test_emp['EDA'], sampling_rate= 250)
#features = {}
#features['CVSD'] = bio['ECG']['HRV']['CVSD']
#features['HF'] = bio['ECG']['HRV']['HF']
#features['HF/P'] = bio['ECG']['HRV']['HF/P']
#features['LF'] = bio['ECG']['HRV']['LF']
#features['LF/HF'] = bio['ECG']['HRV']['LF/HF']
#features['LF/P'] = bio['ECG']['HRV']['LF/P']
#features['LF/n'] = bio['ECG']['HRV']['LFn']
#features['RMSSD'] = bio['ECG']['HRV']['RMSSD']
#features['CVSD'] = bio['ECG']['HRV']['CVSD']
#features['HF'] = bio['ECG']['HRV']['HF']
#features['CVSD'] = bio['ECG']['HRV']['CVSD']
#features['HF'] = bio['ECG']['HRV']['HF']
#features['EDA_mean_amp'] = np.mean(bio['EDA']['SCR_Peaks_Amplitudes'])
#features['EDA_num_peaks'] = len(bio['EDA']['SCR_Peaks_Amplitudes'])

#bio = nk.bio_process(ecg = short_sub['ECG'], eda= short_sub['EDA'])
#bio = nk.bio_process(ecg = test_sub['ECG'], eda= test_sub['EDA'])
def extract_peripheral_features(df): 
    bio = nk.bio_process(ecg= df['ECG'], eda= test_emp['EDA'], sampling_rate= 250)
    features = {}
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
    features['EDA_num_peaks'] = len(bio['EDA']['SCR_Peaks_Amplitudes'])

    return features
    



    
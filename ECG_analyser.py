import neurokit as nk
import pandas as pd
import numpy as np
import seaborn as sns


bio = nk.bio_process(ecg = test_sub['ECG'], eda= test_sub['EDA'])
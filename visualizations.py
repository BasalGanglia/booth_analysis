import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

#  stuff copied and modified from https://www.machinelearningplus.com/time-series/time-series-analysis-python/
# Draw Plot
def plot_df(df, x, y, title="", xlabel='Date', ylabel='Value', dpi=100):
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()
# plot_df(data, data['timestamp'], data['Trust'])
plot_df(trust_dat, trust_dat.index, trust_dat['Trust'])
plot_df(trust_dat, np.arange(len(trust_dat)), trust_dat['Trust'])
plot_df(all_trust, np.arange(len(all_trust)), all_trust['Trust'])

plot_df(all_trust, np.arange(len(all_trust)), all_trust['Trust'])
plot_df(test_sub, np.arange(len(test_sub)), test_sub['ECG'])
plot_df(test_sub, np.arange(400), test_sub.loc[test_sub.index[100:500], 'ECG'])
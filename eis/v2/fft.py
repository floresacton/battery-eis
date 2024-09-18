import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filepaths = []
nums = [1,2,3,5]
for i in nums:
    filepaths.append(f'data\T000{i}ALL.CSV')
data_column_name = 'CH1'
time_column_name = 'TIME'

for filepath in filepaths:
    data_frame = pd.read_csv(filepath, skiprows=15)

    data = data_frame[data_column_name].to_numpy()
    time = data_frame[time_column_name].to_numpy()

    # Find the row indices corresponding to the start and end times
    t_start = -1
    t_end = 1

    start_index = np.argmax(time >= t_start)
    end_index = np.argmax(time >= t_end)

    # Extract the data within the specified time range
    data = data[start_index:end_index]
    time = time[start_index:end_index]

    # get power
    data *= -50

    # filter input signal
    l = 100
    coeffs = np.ones(2*l + 1)
    coeffs = coeffs / np.sum(coeffs)
    data = np.convolve(data, coeffs, mode='same')

    # find mean and subtract from signal before sending to fft
    mean = np.mean(data)
#    data = data - mean

    # calculate fft freq magnitudes
    fft_res = np.fft.fft(data)

    # calculated fft freqs
    sample_period = time[1]-time[0] # Hz
    N = len(data)
    fft_freqs = np.fft.fftfreq(N, sample_period)


    # plot original data
    plt.figure(figsize=(10, 5))

    #plt.subplot(2, 1, 1)
    plt.plot(time, data)
    plt.title('Humanoid Jump')
    plt.xlabel('Time')
    plt.ylabel('Battery Power')

    plt.show()
    quit()

    # Define the cutoff frequencies
    min_freq = 1 / (t_end - t_start)
    print(min_freq)
    max_freq = 500
    idxs = (fft_freqs >= min_freq) & (fft_freqs <= max_freq)

    # Plot the FFT result vs. frequencies
    plt.subplot(2, 1, 2)
    plt.semilogy(fft_freqs[idxs], np.abs(fft_res[idxs]))
    #plt.plot(fft_freqs, np.abs(fft_res))
    plt.title('FFT Result vs. Frequencies')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')

    plt.figtext(0.8, 0.9, filepath, fontsize=12, color='red')

    plt.xticks(np.arange(0, max_freq + 10, 10))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

    # Show the plots
    plt.tight_layout()
    plt.show()


# A mérési adatokat beolvasó program
from csv import reader
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

# with open(input()+'.csv', 'r') as file: ezzel konzolosan is be lehet írni, ha a kódot nem kell megnyyitni


def read_photometry_data(photometry_filename):
    with open(photometry_filename, 'r') as file:
        csv_reader = reader(file)
        list_of_rows = list(csv_reader)
    framecounter = []
    timestamp = []
    data = []
    for i in range(len(list_of_rows[0])-3):
        reg = []
        data.append(reg)
    flags = []
    for row in range(len(list_of_rows)):
        framecounter.append(list_of_rows[row][0])
        timestamp.append(list_of_rows[row][1])
        flags.append(list_of_rows[row][2])
    for i in range(len(list_of_rows[0])-3):
        for row in range(len(list_of_rows)):
            data[i].append(list_of_rows[row][i + 3])
    for j in range(len(data)):
        for k in range(len(data[j])):
            if k == 0:
                continue
            else:
                data[j][k] = float(data[j][k])
        data[j] = data[j][1:]
    timestamp = timestamp[1:]
    for n in range(len(timestamp)):
        timestamp[n] = float(timestamp[n])

    return data, timestamp


def read_digitalin(digitalin_filename):
    with open(digitalin_filename, 'r') as file:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(file)
        list_of_rows = list(csv_reader)
        time = []
        state = []

        for row in range(len(list_of_rows)):
            time.append(list_of_rows[row][0])
            state.append(list_of_rows[row][1])
        for i in range(len(time)):
            time[i] = float(time[i])
    return time


def extract_stim_frames(timestamps, stim_times, data_frames):
    extracted_stim_times = []
    stim_frames = []
    for i in range(len(stim_times)):
        for j in range(len(timestamps)):
            if j > 0:
                if timestamps[j-1] < stim_times[i] and timestamps[j] > stim_times[i]:
                    extracted_stim_times.append(timestamps[j])
                    stim_frames.append(data_frames[j-22:j+26])
    # return extracted_stim_times
    return stim_frames


def extract_frame_rate(timestamps):
    frame_rate = timestamps[1]-timestamps[0]
    return frame_rate


def biexponential_decay(x, a, b, c , d, e):
    return a * np.exp(-b * x) + c * np.exp(-d * x) + e


data_470, timestamp_470 = read_photometry_data(r'D:\phd\data\Photometry\Test\2021.05.07. Stimulus synchronization test\2021_05_07_470_1')
data_415, timestamp_415 = read_photometry_data(r'D:\phd\data\Photometry\Test\2021.05.07. Stimulus synchronization test\2021_05_07_415_1')
stimulus_times = read_digitalin(r'd:\phd\data\Photometry\Test\2021.05.07. Stimulus synchronization test\2021_05_07_digitalin_1')
plotting_470 = data_470[2]
plotting_415 = data_415[2]

frame_rate = extract_frame_rate(timestamp_470)
stimulus_length = 0.2
stimulus_frames = extract_stim_frames(timestamp_470, stimulus_times, data_470[2])
stimulus_frames = np.array(stimulus_frames)
stimulus_average = np.mean(stimulus_frames, axis=0)
stimulus_std = np.std(stimulus_frames, axis=0)
stim_std_plus = stimulus_average + stimulus_std
stim_std_minus = stimulus_average - stimulus_std

random_samples = data_470[2]
np.random.shuffle(random_samples)
random_frames = extract_stim_frames(timestamp_470, stimulus_times, random_samples)
random_frames = np.array(random_frames)
random_average = np.mean(random_frames, axis=0)
random_std = np.std(random_frames, axis=0)
random_std_plus = random_average + random_std
random_std_minus = random_average - random_std


# minimum = min(len(data_415[2]), len(data_470[2]))
# x = np.linspace(0, minimum, minimum+1)
# p0 = (1.0, 1.0, 1.0, 1.0, 1.0)
# params, cv = curve_fit(biexponential_decay, x, data_415[2], p0)
# a, b, c, d, e = params
sampling_freq = 20
# x_coords = np.linspace(0, minimum/sampling_freq, minimum)
x_coords = np.linspace(0, len(stimulus_average)/sampling_freq, len(stimulus_average))

plt.plot(x_coords, stimulus_average, 'b', label='recorded\ndata')
plt.plot(x_coords, stim_std_plus, 'b:', label='+- std')
plt.plot(x_coords, stim_std_minus, 'b:')
plt.plot(x_coords, random_average, 'r', label='randomized\ndata')
plt.plot(x_coords, random_std_plus, 'r:', label='+-std')
plt.plot(x_coords, random_std_minus, 'r:')
plt.axvline(x_coords[1], 0, 0.1, color='g', label='stim times')
plt.axvline(x_coords[21], 0, 0.1, color='g')
plt.axvline(x_coords[41], 0, 0.1, color='g')
# plt.plot(x_coords, plotting_470, label='470nm')
# plt.plot(x_coords, plotting_415, 'red', label='415nm')
plt.xlabel('[sec]')
plt.ylabel('intensity')
# plt.plot(x, biexponential_decay(x, a, b, c, d, e), 'red', label='fitted')
plt.legend(loc='upper right', bbox_to_anchor=(0.85, 0.98))
plt.show()


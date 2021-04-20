#A mérési adatokat beolvasó program
from csv import reader
import matplotlib.pyplot as plt

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
    return data


data_470 = read_photometry_data(r'C:\Data\Neurophotometrics\Recordings\2021_03_26\2021_03_26_470_0.csv')
plotting = data_470[6][4:]

plt.plot(plotting)
plt.show()


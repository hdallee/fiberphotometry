#A digitalin típusú adatokat beolvasó program
from csv import reader
with open('2021_03_26_digitalin_0.csv', 'r') as file:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(file)
    list_of_rows = list(csv_reader)
    time = []
    state = []

    for row in range(len(list_of_rows)):
        time.append(list_of_rows[row][0])
        state.append(list_of_rows[row][1])


print(time)
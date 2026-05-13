import numpy as np

values = []

with open('IO_To_Numpy_Assets_Test.txt', 'r') as file:
    asset_file = file.readlines()
    for line in asset_file:
        split_line = line.split(':')
        value = int(split_line[-1].strip())
        values.append(value)

arr = np.array(values)
print(arr)
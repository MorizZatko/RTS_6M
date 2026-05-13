import numpy as np

arr = np.random.randint(0, 255, size=(5, 3))


red_channel = arr[:, 0]
green_channel = arr[:, 1]
blue_channel = arr[:, 2]
bgr_arr = arr[:, [2, 1, 0]]
av_row = np.mean(arr, axis=1)
bgr_split = np.column_stack((av_row, bgr_arr[:, :2]))

print(f"Orginal RGB Channels: \n", arr)
print(f"Red Channel: ", red_channel)
print(f"Blue Channel: ", blue_channel)
print(f"BGR Channel: \n", bgr_arr)
print(f"Average per line: \n", av_row)
print(f"New format: \n", bgr_split)

import os
import struct
import numpy as np
from tqdm import tqdm

FILEPATH = os.path.join("distortion", "distortion_data.dat")

print(f"opening {FILEPATH}")
with open(FILEPATH, "rb") as file:
    raw_data = file.read()

print("loading data")
data = np.array(list(struct.iter_unpack("f", raw_data))).flatten()


if not len(data) >= 2:
    raise ValueError(f"data is unreasonably small: {len(data)}")

print("extracting metadata")
metadata = data[:2]
data = data[2:]
frame_width = int(metadata[0])
frame_height = int(metadata[1])
num_frames = len(data) / (frame_width * frame_height * 2)

if not num_frames.is_integer():
    raise ValueError(f"the data is not matching the frame size: {num_frames}")

num_frames = int(num_frames)

print("split data into single frames")
data = np.split(data, num_frames)

print("split every frame according to color data and process it")
for i, element in enumerate(tqdm(data)):
    data[i] = np.split(element, len(element) / 2)

import os
import struct
import numpy as np
import numpngw
import click
from tqdm import tqdm
from hurry.filesize import size

# parameters
filepath = os.path.join("distortion", "distortion_data_02.dat")
out = os.path.join("distortion", "img")
in_framerate = 60
out_framerate = 30


# fmt: off
@click.command()
@click.option('--filepath', type=click.Path(exists=True, dir_okay=False), help="the path to the distortion data file", required=True)
@click.option('--out', type=click.Path(file_okay=False), help="the path at which to store the images", required=True)
@click.option('--in_framerate', type=int, help="the framerate used for recording in the browser", required=True)
@click.option('--out_framerate', type=int, help="the framerate of the output", required=True)
# fmt: on
def main(filepath: str, out: str, in_framerate: int, out_framerate: int):
    if out_framerate > in_framerate or not (in_framerate / out_framerate).is_integer():
        raise ValueError("out_framerate must be a factor of in_framerate")

    # open data binary file
    print(f"opening {filepath}")
    with open(filepath, "rb") as file:
        raw_data = file.read()

    # load data into array and flatten it to one dimenstion ([float_0, float_1, ... , float_n])
    print("loading data")
    data = np.array(
        list(tqdm(struct.iter_unpack("f", raw_data), total=int(len(raw_data) / 4)))
    ).flatten()
    print(f"loaded {size(len(data))}")

    # error, if not enough data is present
    if not len(data) >= 2:
        raise ValueError(f"data is unreasonably small: {len(data)}")

    # extract frame size
    print("extracting metadata")
    metadata = data[:2]
    data = data[2:]
    frame_width = int(metadata[0])
    frame_height = int(metadata[1])
    num_frames = len(data) / (frame_width * frame_height * 2)
    print(f"frame width: {frame_width}, height: {frame_height}")

    # error, if incomplete frame at the end
    if not num_frames.is_integer():
        raise ValueError(f"the data is not matching the frame size: {num_frames}")

    num_frames = int(num_frames)

    # split data into frames
    print("split data into single frames")
    data = np.split(data, num_frames)
    print(f"frame count: {num_frames}")

    # remove frames according to out framerate
    print("remove frames, if framerate change requires it")
    mask = list(range(0, len(data), int(in_framerate / out_framerate)))
    data = [element for index, element in enumerate(data) if index in mask]
    print(f"new frame count: {len(data)}")

    # split frame data into 16 bit RGB pixels
    print("split every frame according to color data and process it")
    for i, frame in enumerate(tqdm(data)):
        data[i] = np.flip(
            np.array(
                [np.append(p, 0) for p in np.split(frame, len(frame) / 2)]
            ).reshape(frame_height, frame_width, 3),
            0,
        )

    data = ((np.array(data) + 0.5) * np.iinfo(np.uint16).max).astype(np.uint16)

    # create outdir, if it does not exist yet
    os.makedirs(out, exist_ok=True)

    # save data to pngs
    print(f"saving frames to: {out}")
    for index, frame in enumerate(tqdm(data)):
        numpngw.write_png(
            os.path.join(out, f"{str(index).zfill(len(str(len(data))))}.png"), frame
        )


if __name__ == "__main__":
    main()

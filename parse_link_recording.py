from typing import Union

import os
import glob
import struct
import numpy as np
import click
from tqdm import tqdm
from hurry.filesize import size
from itertools import chain

# parameters
filepath = os.path.join("distortion", "distortion_data_02.dat")
out = os.path.join("distortion", "img")
in_framerate = 60
out_framerate = 30


# fmt: off
@click.command()
@click.option('--dir', type=click.Path(exists=True, file_okay=False), help="directory containing the files to be parsed & concatted", required=True)
@click.option('--out', type=click.Path(dir_okay=False), help="where to save to result", required=True)
@click.option('--in_framerate', type=int, help="the framerate used for recording in the browser", required=True)
@click.option('--out_framerate', type=int, help="the framerate of the output", required=True)
@click.option('--max', type=click.FloatRange(0.0, 1.0), help="the maximum value, the colors are scaled to", required=False)
# fmt: on
def main(
    dir: str,
    out: str,
    in_framerate: int,
    out_framerate: int,
    max: Union[float, None],
):
    if out_framerate > in_framerate or not (in_framerate / out_framerate).is_integer():
        raise ValueError("out_framerate must be a factor of in_framerate")

    # open data binary file
    print(f"opening {dir}")
    data = []
    frame_width = 0
    frame_height = 0
    for path in sorted(glob.glob(os.path.join(dir, "*.dat"))):
        with open(path, "rb") as file:
            raw_data = file.read()

        # load data into array and flatten it to one dimenstion ([float_0, float_1, ... , float_n])
        print(f"loading data from {path}")
        sequence = np.array(
            list(tqdm(struct.iter_unpack("f", raw_data), total=int(len(raw_data) / 4)))
        ).flatten()
        print(f"loaded {size(len(sequence))}")

        # error, if not enough data is present
        if not len(sequence) >= 2:
            raise ValueError(f"data is unreasonably small: {len(sequence)}")

        # extract frame size
        print("extracting metadata")
        metadata = sequence[:2]
        sequence = sequence[2:]
        if not frame_width:
            frame_width = int(metadata[0])
            frame_height = int(metadata[1])

            print(f"frame width: {frame_width}, height: {frame_height}")
        else:
            if frame_width != int(metadata[0]) or frame_height != int(metadata[1]):
                raise ValueError("frame dimension mismatch detected")

        # scaling accordingly max value
        if max:
            print(f"max value is {max}. scaling accordingly")
            sequence *= 1 / max
            sequence = np.clip(sequence, -1.0, 1.0)

        sequence = sequence.tolist()

        # remove frames according to out framerate
        print("remove frames, if framerate change requires it")
        if out_framerate != in_framerate:
            sequence = [
                element
                for index, element in enumerate(tqdm(sequence))
                if int(index / (frame_width * frame_height * 2))
                % int(in_framerate / out_framerate)
                == 0
            ]
            print(f"new size: {size(len(sequence))}")

        data.append(sequence)

    print(f"concatenating {len(data)} sequences")
    data = [float(frame_width), float(frame_height), *list(chain.from_iterable(data))]

    # create outdir, if it does not exist yet
    os.makedirs(os.path.dirname(out), exist_ok=True)

    # save data to pngs
    print(f"saving concatted data to: {out}")
    buffer = struct.pack(f"{len(data)}f", *data)
    with open(out, "wb") as file:
        file.write(buffer)


if __name__ == "__main__":
    main()

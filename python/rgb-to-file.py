"""
Save a single frame to jpg.
"""

import argparse
import time
from datetime import datetime
import subprocess
import sys
from PIL import Image
import os
import numpy as np
from matplotlib import cm

RAW_RGB_PATH = "../examples/rawrgb"
DEFAULT_FILENAME = "mlx90640-{}.jpg".format(
    datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
)
DEFAULT_FRAMEDROP = 5


def main():
    parser = argparse.ArgumentParser(description="Save a single capture")
    parser.add_argument(
        "--filename",
        default=DEFAULT_FILENAME,
        type=str,
        help="Name for file, including extension .jpg",
    )
    parser.add_argument(
        "--dropframes",
        default=DEFAULT_FRAMEDROP,
        type=int,
        help="Number of frames to drop, default {}".format(DEFAULT_FRAMEDROP),
    )
    args = parser.parse_args()

    if not os.path.isfile(RAW_RGB_PATH):
        raise RuntimeError(
            '{} doesn\'t exist, did you forget to run "make"?'.format(RAW_RGB_PATH)
        )

    with subprocess.Popen(
        ["sudo", RAW_RGB_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as camera:
        # Despite the docs, we use read() here since we want to poll
        # the process for chunks of 2304 bytes, each of which is a frame
        # Capture two frames and average to remove checkerboard

        frames_to_drop = args.dropframes  # since the camera needs to warm up
        for i in range(frames_to_drop):
            camera.stdout.read(2304)
            print("Capture in {}".format(frames_to_drop - i))

        frame = camera.stdout.read(2304)
        image = Image.frombytes("RGB", (32, 24), frame)
        print("Saving {} ".format(args.filename))
        image.save(args.filename)


if __name__ == "__main__":
    main()

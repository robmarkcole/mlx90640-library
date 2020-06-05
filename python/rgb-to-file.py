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

RAW_RGB_PATH = "../examples/rawrgb"
DEFAULT_FILENAME = "mlx90640-{}.jpg".format(
    datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
)


def main():
    parser = argparse.ArgumentParser(description="Save a single capture")
    parser.add_argument(
        "--filename",
        default=DEFAULT_FILENAME,
        type=str,
        help="Name for file, including extension .jpg",
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
        frame = camera.stdout.read(2304)

        # Convert the raw frame bytes into a PIL image and resize
        image = Image.frombytes("RGB", (24, 32), frame)
        print("Saving {} ".format(args.filename))
        image.save(args.filename)


if __name__ == "__main__":
    main()

"""
Robin edit of rgb-to-gif.py to save a single frame to jpg.
"""

#!/usr/bin/env python3
import time
from datetime import datetime
import subprocess
import sys
from PIL import Image
import os

RAW_RGB_PATH = "../examples/rawrgb"

if not os.path.isfile(RAW_RGB_PATH):
    raise RuntimeError("{} doesn't exist, did you forget to run \"make\"?".format(RAW_RGB_PATH))

with subprocess.Popen(["sudo", RAW_RGB_PATH], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as camera:
	# Despite the docs, we use read() here since we want to poll
        # the process for chunks of 2304 bytes, each of which is a frame
        frame = camera.stdout.read(2304)

        # Convert the raw frame bytes into a PIL image and resize
        image = Image.frombytes('RGB', (24, 32), frame)

        filename = 'mlx90640-{}.jpg'.format(
            datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

        print("Saving {} ".format(filename))
        image.save(filename,)


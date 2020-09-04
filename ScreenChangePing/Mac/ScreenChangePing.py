from subprocess import call
import numpy as np
import time
import cv2
import os

# Define the screen rectangle to capture
TOP = "800"
LEFT = "-250"
WIDTH = "250"
HEIGHT = "500"

PING_SOUND = "/System/Library/Sounds/Pop.aiff"
CHECK_FREQUENCY = 2  # value in seconds
MUTE_AFTER_PING = 10  # value in seconds

if os.path.isfile("screenshotA.png"):
    os.remove("screenshotA.png")
if os.path.isfile("screenshotB.png"):
    os.remove("screenshotB.png")

# Initialize the mute timestamp
mute_until = time.time() + 0

while True:

    call(["screencapture", "-x", "-R" + LEFT + "," + TOP + "," + WIDTH + "," + HEIGHT, "screenshotA.png"])

    if os.path.isfile("screenshotB.png"):
        # Read both screenshots
        imgA = cv2.imread("screenshotA.png")
        imgB = cv2.imread("screenshotB.png")

        # Convert screenshots to greyscale
        imgAGS = cv2.cvtColor(imgA, cv2.COLOR_BGR2GRAY)
        imgBGS = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)

        # Calculate mean square error between two screenshots
        err = np.sum((imgAGS.astype("float") - imgBGS.astype("float")) ** 2)
        err /= float(imgAGS.shape[0] * imgAGS.shape[1])

        # Get the current time
        t = time.time()
        curr_time = time.strftime("%H:%M:%S", time.localtime())

        # If the change in screen snapshots is significant, play a sound (unless muted)
        if err > 50 and t >= mute_until:
            print(curr_time + " - Change Detected. Muting for " + str(MUTE_AFTER_PING) + " seconds.")
            call(["afplay", PING_SOUND])
            # set mute expiry time
            mute_until = t + MUTE_AFTER_PING

    # Rename current screenshot to become the comparison screenshot
    os.replace("screenshotA.png", "screenshotB.png")

    # Sleep before taking the next screenshot
    time.sleep(CHECK_FREQUENCY)

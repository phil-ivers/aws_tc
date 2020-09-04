from playsound import playsound
import numpy as np
import time
import cv2
import os
import mss
import mss.tools

# Define which monitor/display, and what area of that display to capture
DISPLAY = 2
TOP = 500
LEFT = 500
WIDTH = 200
HEIGHT = 500

PING_SOUND = "C:\\WINDOWS\\media\\Windows Balloon.wav"
CHECK_FREQUENCY = 5  # value in seconds
MUTE_AFTER_PING = 10  # value in seconds

if os.path.isfile("screenshotA.png"):
    os.remove("screenshotA.png")
if os.path.isfile("screenshotB.png"):
    os.remove("screenshotB.png")


def take_screenshot(filename):
    with mss.mss() as sct:
        # Which monitor to use
        monitor = sct.monitors[DISPLAY]

        # define the capture rectangle
        left = monitor["left"] + LEFT  # Offset from the left side of the display
        top = monitor["top"] + TOP  # Offset from the top of the display
        right = left + WIDTH  # Width of the rectangle
        lower = top + HEIGHT  # Height of the rectangle
        bbox = (left, top, right, lower)

        im = sct.grab(bbox)  # type: ignore

        mss.tools.to_png(im.rgb, im.size, output=filename)


# Initialize the mute timestamp
mute_until = time.time() + 0

while True:

    take_screenshot("screenshotA.png")

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
            playsound(PING_SOUND)
            # set mute expiry time
            mute_until = t + MUTE_AFTER_PING

    # Rename current screenshot to become the comparison screenshot
    os.replace("screenshotA.png", "screenshotB.png")

    # Sleep before taking the next screenshot
    time.sleep(CHECK_FREQUENCY)

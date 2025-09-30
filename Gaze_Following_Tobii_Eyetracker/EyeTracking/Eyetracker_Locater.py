import os
#from psychopy import core, visual, sound, event, monitors

import pandas as pd

import tobii_research as tr



## Eyetracker set up--------------------------------------------------------------------------------------------------------------

# Locate an eyetracker if it is hooked up, yields boolean value
found_eyetracker = tr.find_all_eyetrackers()


if found_eyetracker == True: # If there is an eyetracker then...
    eyetracker = found_eyetracker[0] # Create the eyetracker object
    print(eyetracker)
else:
    print("No eyetracker detected")



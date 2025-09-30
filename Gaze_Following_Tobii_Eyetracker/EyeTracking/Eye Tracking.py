import os
from psychopy import core, visual, sound, event, monitors

import pandas as pd

import tobii_research as tr

# Set up monitor, only needed for VS Code
monitor_name = 'Matt Monitor'
my_monitor = monitors.Monitor(monitor_name)
my_monitor.setSizePix((1920, 1080))  # Set to your monitor's resolution
my_monitor.setWidth(53.1)  # Set to your monitor's width in cm
my_monitor.setDistance(60)  # Set to your viewing distance in cm
my_monitor.save()

# Set up the window screen
winsize = (960, 540)
win = visual.Window(size = winsize, units = 'pix', pos = (0,30))
# Add screen = 2, which will be the eye tracker

# Set the working directory
os.chdir(r'C:/Users/Laurent Pretot/Desktop/MADE_YOU_LOOK_v1/EyeTracking')

# Create your stimuli
fixation = visual.ImageStim(win, 'EXP\\Stimuli\\fixation.png', size = (200, 200))
square = visual.ImageStim(win, 'EXP\\Stimuli\\square.png', size = (200, 200))
circle = visual.ImageStim(win, 'EXP\\Stimuli\\circle.png', size = (200, 200))

winning = visual.ImageStim(win, 'EXP\\Stimuli\\winning.png', size = (200, 200), pos = (500, 0))
losing = visual.ImageStim(win, 'EXP\\Stimuli\\loosing.png', size = (200, 200), pos = (-500, 0))

# Create your sounds
winning_sound = sound.Sound("EXP\\Stimuli\\winning.wav")
losing_sound = sound.Sound("EXP\\Stimuli\\loosing.wav")

# Create arrays to hold characters and sounds
cues = [circle, square]
rewards = [winning, losing]
sounds = [winning_sound, losing_sound]

# Create Trial Array
Trials = [1, 0, 1, 0, 1, 0]

# Set up Data Output File
monkey = "Matt"

def makeFileName(task='Task', format='csv'):
    return monkey + '_' + task + '_' + '.' + format

output_file_name = makeFileName('Eyetracking Data')

## Eyetracker set up--------------------------------------------------------------------------------------------------------------

# Locate an eyetracker if it is hooked up, yields boolean value
found_eyetracker = tr.find_all_eyetrackers()


if found_eyetracker == True: # If there is an eyetracker then...
    eyetracker = found_eyetracker[0] # Create the eyetracker object

gaze_data_buffer = [] # this empty array will store all the variables we are interested in
trigger = ""  # this tells us what was occurring in the program at the time of the eye look


def gaze_data_callback(gaze_data):
    global gaze_data_buffer
    global trigger
    global winsize

    t = gaze_data.system_time_stamp / 1000.0 # Get time in ms instead of micro seconds
    # (0,0 is top left of tobi screen)
    lx = winsize[0] - gaze_data.left_eye.gaze_point.position_on_display_area[0] * winsize[0] # First coordinate = x as a pixel number
    ly = winsize[1] - gaze_data.left_eye.gaze_point.position_on_display_area[1] * winsize[1] # Second coordinate = y as a pixel number

    rx = winsize[0] - gaze_data.right_eye.gaze_point.position_on_display_area[0] * winsize[0] # x coord of right eye
    ry = winsize[1] - gaze_data.right_eye.gaze_point.position_on_display_area[1] * winsize[1] # y coord of right eye

    lvalid = gaze_data.left_eye.gaze_point.validity 
    rvalid = gaze_data.right_eye.gaze_point.validity 

    lpupil = gaze_data.left_eye.pupil.diameter # L pupil diameter
    rpupil = gaze_data.right_eye.pupil.diameter # R pupil diameter

    gaze_data_buffer.append((t, lx, ly, rx, ry, lvalid, rvalid, lpupil, rpupil, trigger)) # Creates an array of all these data points, 

def save_data(buffer, file_name):
    # Make a copy of the buffer and clear it
    buffer_copy = buffer[:] # we will only work on the copy while the new empty buffer will be collecting data
    buffer.clear() # clear the buffer so that it can collect new data
    
    # Define column names for the dataframe
    # make sure theyre in the same order as gaze_data_buffer[]
    columns = ['time', 'L_X', 'L_Y', 'R_X', 'R_Y', 'L_Validity', 'R_Validity', 'L_Pupil', 'R_Pupil', 'Trigger']

    # Convert buffer to DataFrame
    out = pd.DataFrame(buffer_copy, columns=columns)
    
    # Check if the file exists
    file_exists = not os.path.isfile(file_name)
    
    # Write the DataFrame to an HDF5 file and only include header if the file does not exist
    out.to_csv(file_name, mode='a', index = False, header = file_exists)


# Collect Data Here -----------------------------------------------------------------------

# Sample at the frquency of the Tobii eye tracker
# x 300 Hz will run this 300 times per second
if found_eyetracker:
    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

## Run the Game ------------------------------------------------------------------------------------------------------------

trigger = 'experiment start'

for trial in Trials:
    win.flip()

    fixation.draw()
    print("Drawing fixation")
    win.flip()
    print("Waiting for 3")
    core.wait(1)

    win.flip()

    cues[trial].draw()

    if trial == 0:
        trigger = "None"

    if trial == 1:
        trigger = "Wren"

    print("Drawing circle")
    win.flip()
    core.wait(3)

    win.flip()

    rewards[trial].draw()
    win.flip()
    core.wait(3)

    print("Playing the losing sound")
    losing_sound.play()

    keys = event.getKeys()
    if 'escape' in keys:
        win.close()
        core.quit()
    
    if 'q' in keys:
        win.close()
        core.quit()

    # ISI
    clock = core.Clock() # Start the clock
    if found_eyetracker == True: # If there is an eyetracker,
        save_data(gaze_data_buffer, output_file_name) # Save the data every time it loops (300 times per second)
    while clock.getTime() < 1: # Set ISI = 1 and wait that remaining time
        pass

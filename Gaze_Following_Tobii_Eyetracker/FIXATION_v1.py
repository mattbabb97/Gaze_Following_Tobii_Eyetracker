# _   .-')      ('-.     _ .-') _     ('-.                                                                                        .-. .-')   
#( '.( OO )_   ( OO ).-.( (  OO) )  _(  OO)                                                                                       \  ( OO )  
# ,--.   ,--.) / . --. / \     .'_ (,------.        ,--.   ,--..-'),-----.  ,--. ,--.          ,--.      .-'),-----.  .-'),-----. ,--. ,--.  
# |   `.'   |  | \-.  \  ,`'--..._) |  .---'         \  `.'  /( OO'  .-.  ' |  | |  |          |  |.-') ( OO'  .-.  '( OO'  .-.  '|  .'   /  
# |         |.-'-'  |  | |  |  \  ' |  |           .-')     / /   |  | |  | |  | | .-')        |  | OO )/   |  | |  |/   |  | |  ||      /,  
# |  |'.'|  | \| |_.'  | |  |   ' |(|  '--.       (OO  \   /  \_) |  |\|  | |  |_|( OO )       |  |`-' |\_) |  |\|  |\_) |  |\|  ||     ' _) 
# |  |   |  |  |  .-.  | |  |   / : |  .--'        |   /  /     \ |  | |  | |  | | `-' /      (|  '---.'  \ |  | |  |  \ |  | |  ||  .   \   
# |  |   |  |  |  | |  | |  '--'  / |  `---.       `-./  /       `'  '-'  '('  '-'(_.-'        |      |    `'  '-'  '   `'  '-'  '|  |\   \  
# `--'   `--'  `--' `--' `-------'  `------'         `--'          `-----'   `-----'           `------'      `-----'      `-----' `--' '--'  
# CODE BY MATTHEW H. BABB ALL RIGHTS RESERVED !!!!!!!!!!!!
# Do NOT use this code without the permission of original author !!!!!!!!!!!!
                                                                                                                                
import sys                  # Import the 'system' library
import random               # Import the 'random' library which gives cool functions for randomizing numbers
from random import choice
import math                 # Import the 'math' library for more advanced math operations
import time                 # Import the 'time' library for functions of keeping track of time (ITIs, IBIs etc.)
import datetime
import os                   # Import the operating system (OS)
import glob                 # Import the glob function
import pygame               # Import Pygame to have access to all those cool functions
import Matts_Toolbox        # Import Matt's Toolbox with LRC specific functions
import cv2
import tobii_research as tr


pygame.init()               # This initializes all pygame modules

"""READ FILES ------------------------------------------------------------------------------------------------------"""

# Read the monkey name from monkey.txt which should be located inside your program's folder
with open("monkey.txt") as f:
    monkey = f.read()

# Set Current Date
today = time.strftime('%Y-%m-%d')

"""SET UP LOCAL VARIABLES ---------------------------------------------------------------------------------------------"""

white = (255, 255, 255)                                         # This sets up colors you might need
blue = (0, 191, 255)
black = (0, 0, 0)                                               # Format is (Red, Green, Blue, Alpha)
green = (0, 200, 0)                                             # 0 is the minimum & 260 is the maximum
red = (250, 0, 0)                                               # Alpha is the transparency of a color
transparent = (0, 0, 0, 0)

"""Put your sounds here"""
sound_chime = pygame.mixer.Sound("chime.wav")                   # This sets your trial initiation sound
sound_correct = pygame.mixer.Sound("correct.wav")               # This sets your correct pellet dispensing sound
sound_incorrect = pygame.mixer.Sound("Incorrect.wav")           # This sets your incorrect sound
sound_sparkle = pygame.mixer.Sound("sparkle.wav")               # Any sound can be added, just make sure it is a .wav file and it is in your program's folder

"""Put your Screen Parameters here"""
scrSize = (800, 600)                                            # Standard Resolution of Monkey Computers is 800 x 600. This changes for the joint computers.
scrRect = pygame.Rect((0, 0), scrSize)                          # Sets the shape of the screen to be a rectangle
fps = 60                                                        # Frames Per Second. Typically = 60. Changing this changes the cursor speed.

"""EYETRACKER SETUP -------------------------------------------------------------------------------------------------"""

found_eyetrackers = tr.find_all_eyetrackers()

eyetracker = found_eyetrackers[0]        # Create the eyetracker object

gaze_data_buffer = []                       # this empty array will store all the variables we are interested in
trigger = ""                                # this tells us what was occurring in the program at the time of the eye look


"""FILE MANIPULATION FUNCTIONS --------------------------------------------------------------------------------------"""

# Create an Output File
from Matts_Toolbox import writeLn

# Name the file of your Data Output
from Matts_Toolbox import makeFileName

# Get parameters from parameters.txt
from Matts_Toolbox import getParams

# Save parameters into their own file for safe keeping
from Matts_Toolbox import saveParams

"""SCREEN MANIPULATION FUNCTIONS ------------------------------------------------------------------------------------"""
from Matts_Toolbox import setScreen

from Matts_Toolbox import refresh

"""HELPER FUNCTIONS -------------------------------------------------------------------------------------------------"""
# Quit Program Function
from Matts_Toolbox import quitEscQ

# Sound Playing Function
from Matts_Toolbox import sound

# Pellet Dispensing Function
from Matts_Toolbox import pellet

# Moving the Cursor
from Matts_Toolbox import joyCount
from Matts_Toolbox import moveCursor

# Randomization Functions
from Matts_Toolbox import pseudorandomize
from Matts_Toolbox import shuffle_array

"""LIST OF TODOS ----------------------------------------------------------------------------------------------------"""

# TODO: Work on writing data into excel file
# TODO: Check to make sure training parameters work
# TODO: Delete excess/unused code
# TODO: Remove print() statements for seconds

""" ICON CLASS -------------------------------------------------------------------------------------------------------"""

from Matts_Toolbox import Box
# This imports the class of Box from my tool box, which can then be used to make things on the screen
# Objects of class "Box" have certain characteristics, such as size and pixels.

# For more information on Classes, Objects, and Inheritence, you can search up "Object Oriented Programing in Python"

# Create a NEW CLASS called "ICON" which INHERITS the characteristics of class "Box"
    # You will create objects with class "Icon" to draw things on the screen that the monkeys can interact with
class Icon(Box):
    def __init__(self, PNG, position, scale):                           # To create an object you need to provide the code with the following:
                                                                            # 1. The item's image, typically a .png file
                                                                            # 2. The item's (x,y) position
                                                                            # 3. The item's size (scale)
        super(Icon, self).__init__()
        image = pygame.image.load(PNG).convert_alpha()                          # image = image you passed in arguments
        self.size = image.get_size()                                            # Get the size of the image
        self.image = pygame.transform.smoothscale(image, scale)                 # Scale the image = scale inputted
        self.rect = self.image.get_rect()                                       # Get rectangle around the image
        self.rect.center = self.position = position                             # Set rectangle and center at position
        self.mask = pygame.mask.from_surface(self.image)                        # Creates a mask object
        
    """Objects of the Icon class have this .mv2pos function"""
    """This function allows you to move the Icon anywhere on the screen"""
    def mv2pos(self, position):
        self.rect = self.image.get_rect()
        self.rect.center = self.position = position


""" TRIAL CLASS -----------------------------------------------------------------------------------------------------"""
class Trial(object):
    def __init__(self):
        super(Trial, self).__init__()
        self.train_or_test = train_or_test                  # Determine if this is a Training or a Testing Condition by pulling the value of train_or_test from parameters.txt
        self.pre_test = True
        self.trial_number = 0                               # Trial Number {1 - x}
        self.trial_within_block = -1                        # Trial Within the current block {0 - x}
        self.block = 1
        self.blocks_per_session = blocks_per_session        # Number of blocks per session = stored in parameters.txt
        self.start_time = 0
        self.which_video = 1
        self.video_playtime = 0.00

        self.recording = False
        self.et_start_time = None

        with open("trials_social.txt") as a:
            self.social_trial_count = int(a.read())
        with open("trials_asocial.txt") as b:
            self.asocial_trial_count = int(b.read())
        with open("trials_asocial_eyes.txt") as c:
            self.asocial_eyes_trial_count = int(c.read())
        with open("trial_count_total.txt") as d:
            self.total_trials = int(d.read())

        # Keep Track of Phases
        self.startphase = True                              # Start button
        self.phase1 = False                                 # Phase 1: Stimuli flashes for 5 sec
        self.phase2 = False                                 # Phase 2: Blank Screen
        self.phase3 = False                                 # Phase 3: Display Stimuli
        self.phase4 = False                                 # Phase 4: NA
        self.phase5 = False                                 # Phase 5: NA
        self.phase6 = False                                 # Phase 6: NA
        
        # Keep Track of events that occur inside the program
        self.event1 = False
        self.event2 = False
        self.event3 = False

        # Set up the program's stimuli files
        self.pngs = glob.glob('stimuli/*.png')              # Make a list of the .png files from the stimuli folder
        self.stimuli_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]   # Make a list of all 10 stimuli indices [label 0 - 9]
        random.shuffle(self.stimuli_idx)                    # Shuffle the order of the stimuli list
        self.stimID = -1                                    # stimID tells you which stimuli you are pulling within the stimuli_idx list
        

        self.random_number_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.motivation_array = [1, 2, 3, 4]
        self.social_array = [5, 6]
        self.asocial_array = [7, 8]
        self.asocial_eyes_array = [9, 10]
        
        if self.pre_test == True:
            self.block_length = 20
            #PROGRAM TROUBLESHOOTING
            #self.trial_type = [5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
            self.trial_type = [1, 2, 3, 4, 5]
            pseudorandomize(self.trial_type)
        elif self.pre_test == False:
            self.block_length = 72
            self.trial_type_1 =  [random.choice(self.motivation_array), 6, random.choice(self.motivation_array), 8, random.choice(self.motivation_array), 9]
            self.trial_type_2 =  [random.choice(self.motivation_array), 5, random.choice(self.motivation_array), 10, random.choice(self.motivation_array), 8]
            self.trial_type_3 =  [random.choice(self.motivation_array), 7, random.choice(self.motivation_array), 6, random.choice(self.motivation_array), 9]
            self.trial_type_4 =  [random.choice(self.motivation_array), 8, random.choice(self.motivation_array), 10, random.choice(self.motivation_array), 5]
            self.trial_type_5 =  [random.choice(self.motivation_array), 10, random.choice(self.motivation_array), 5, random.choice(self.motivation_array), 7]
            self.trial_type_6 =  [random.choice(self.motivation_array), 9, random.choice(self.motivation_array), 7, random.choice(self.motivation_array), 6]
            self.trial_type_7 =  [random.choice(self.motivation_array), 5, random.choice(self.motivation_array), 7, random.choice(self.motivation_array), 10]
            self.trial_type_8 =  [random.choice(self.motivation_array), 6, random.choice(self.motivation_array), 9, random.choice(self.motivation_array), 7]
            self.trial_type_9 =  [random.choice(self.motivation_array), 7, random.choice(self.motivation_array), 5, random.choice(self.motivation_array), 10]
            self.trial_type_10 = [random.choice(self.motivation_array), 8, random.choice(self.motivation_array), 9, random.choice(self.motivation_array), 6]
            self.trial_type_11 = [random.choice(self.motivation_array), 10, random.choice(self.motivation_array), 6, random.choice(self.motivation_array), 8]
            self.trial_type_12 = [random.choice(self.motivation_array), 9, random.choice(self.motivation_array), 8, random.choice(self.motivation_array), 5]

            self.random_number = random.choice(self.random_number_array)
            if self.random_number == 1:
                self.trial_type = self.trial_type_1 + self.trial_type_2 + self.trial_type_3 + self.trial_type_4 + self.trial_type_5 + self.trial_type_6 + self.trial_type_7 + self.trial_type_8 + self.trial_type_9 + self.trial_type_10 + self.trial_type_11 + self.trial_type_12
            elif self.random_number == 2:
                self.trial_type = self.trial_type_9 + self.trial_type_3 + self.trial_type_5 + self.trial_type_11 + self.trial_type_2 + self.trial_type_10 + self.trial_type_4 + self.trial_type_1 + self.trial_type_7 + self.trial_type_6 + self.trial_type_8 + self.trial_type_12
            elif self.random_number == 3:
                self.trial_type = self.trial_type_4 + self.trial_type_8 + self.trial_type_2 + self.trial_type_12 + self.trial_type_7 + self.trial_type_1 + self.trial_type_10 + self.trial_type_6 + self.trial_type_5 + self.trial_type_9 + self.trial_type_3 + self.trial_type_11
            elif self.random_number == 4:
                self.trial_type = self.trial_type_6 + self.trial_type_2 + self.trial_type_11 + self.trial_type_8 + self.trial_type_1 + self.trial_type_12 + self.trial_type_5 + self.trial_type_10 + self.trial_type_3 + self.trial_type_7 + self.trial_type_4 + self.trial_type_9
            elif self.random_number == 5:
                self.trial_type = self.trial_type_5 + self.trial_type_7 + self.trial_type_1 + self.trial_type_9 + self.trial_type_3 + self.trial_type_11 + self.trial_type_8 + self.trial_type_6 + self.trial_type_2 + self.trial_type_12 + self.trial_type_10 + self.trial_type_4
            elif self.random_number == 6:
                self.trial_type = self.trial_type_12 + self.trial_type_1 + self.trial_type_10 + self.trial_type_2 + self.trial_type_8 + self.trial_type_5 + self.trial_type_11 + self.trial_type_9 + self.trial_type_4 + self.trial_type_3 + self.trial_type_6 + self.trial_type_7
            elif self.random_number == 7:
                self.trial_type = self.trial_type_8 + self.trial_type_4 + self.trial_type_6 + self.trial_type_10 + self.trial_type_1 + self.trial_type_3 + self.trial_type_7 + self.trial_type_12 + self.trial_type_2 + self.trial_type_5 + self.trial_type_9 + self.trial_type_11
            elif self.random_number == 8:
                self.trial_type = self.trial_type_11 + self.trial_type_9 + self.trial_type_4 + self.trial_type_2 + self.trial_type_12 + self.trial_type_5 + self.trial_type_1 + self.trial_type_7 + self.trial_type_10 + self.trial_type_3 + self.trial_type_6 + self.trial_type_8
            elif self.random_number == 9:
                self.trial_type = self.trial_type_10 + self.trial_type_5 + self.trial_type_3 + self.trial_type_7 + self.trial_type_12 + self.trial_type_4 + self.trial_type_8 + self.trial_type_2 + self.trial_type_11 + self.trial_type_6 + self.trial_type_1 + self.trial_type_9
            elif self.random_number == 10:
                self.trial_type = self.trial_type_3 + self.trial_type_11 + self.trial_type_7 + self.trial_type_1 + self.trial_type_5 + self.trial_type_9 + self.trial_type_2 + self.trial_type_12 + self.trial_type_6 + self.trial_type_8 + self.trial_type_10 + self.trial_type_4

                                                                                            
        # Keep Track of Training Performance
            # This is useful if you want to advance a monkey to a different condition after they acheive 80% success
            # For example, at the end of a block you can divide num_correct by number of trials in a block to get the correct_pct
        self.num_correct = 0
        self.correct_pct = 0.00 
        self.consecutive = 0

        # Set up a blank list for the trial's stimuli; We will fill it with simuli later
        self.stimuli = []
        # Set up the stimuli (x,y) positions on the screen
        self.icon_position = [(100, 100), (700, 100), (100, 500), (700, 500), (400, 300)]

        # Set up any Time Intervals for the program (i.e. delays, phase durations, etc.)
        self.delay_interval = [5, 10, 5, 10, 5, 10, 5, 10, 5, 10, 5, 10, 5, 10, 5, 10, 5, 10, 5, 10, 5, 10, 5, 10]
        self.target_timer = 4.000   # The length of time the stimuli is presented for learning
        self.hint_timer = 5.000     # The length of time the hint is available for selection


    """Now that you have created your "Trial" class and given it all the attributes you want, it is time to give all objects of the "Trial" class access to FUNCTIONS
    Functions are a way for things to happen in the program. They can start a new trial, draw stimuli, or even make stimuli dance on the screen"""
    def gaze_data_callback(self, gaze_data):
        left = gaze_data['left_gaze_point_on_display_area']
        right = gaze_data['right_gaze_point_on_display_area']
        timestamp = gaze_data['device_time_stamp']   # or time.time() if you prefer system time

        if left and right:
            #row = [self.total_trials, monkey, today, self.trial_number, self.trial_type[self.trial_within_block],
            #       self.video_playtime, self.which_video,
            #       self.phase1, self.phase2,
            #       timestamp,
            #       round(left[0], 3), round(left[1], 3),
            #       round(right[0], 3), round(right[1], 3)]
            row = [self.total_trials, monkey, today, self.trial_number, self.trial_type[self.trial_within_block],
                   0, 0, self.phase1, self.phase2,
                   timestamp,
                   round(left[0], 3), round(left[1], 3),
                   round(right[0], 3), round(right[1], 3)]
            writeLn(eye_data_file, row)

        if left and right:  # Check that data is valid (not None)
            print("Left eye: ({:.3f}, {:.3f}) \t Right eye: ({:.3f}, {:.3f})".format(
                left[0], left[1], right[0], right[1]))
        else:
            print("Gaze data not available.")

    def new(self):
        """Locate Eyetracker"""
        print("Successfully connected to: ", eyetracker.serial_number)
        """Start a new trial"""
        global start_time
        global SELECT
        SELECT = -1
        self.trial_number += 1                                                  # Increment trial number by 1
        self.trial_within_block += 1                                            # Increment trial within block by 1
        self.stimID += 1                                                        # Incremebt stimID by 1 to move to the next stimuli
        sound_chime.play()
        cursor.mv2pos((400, 200))
        print("Trial: " + str(self.trial_number))                               # Print the information to the console
        print("Trial_within_block: " + str(self.trial_within_block))                # NOTE: This does not print the information to an excel sheet
        #print("Block: " + str(self.block))                                          # We will use another function to do that
        print("Trial Type Array: " + str(self.trial_type))

        if self.trial_within_block == self.block_length:                        # If this is the last trial in the block
            self.trial_within_block = 0                                         # Reset this to 0           
            self.newBlock()                                                     # Run the function .newBlock()
            print("Block Complete!")                                            # Print "Block Complete!" to the console


        # Reset all phases to False except the Start Phase
        self.startphase = True                              # Start button
        self.phase1 = False                                 # Phase 1: Stimuli flashes for 5 sec
        self.phase2 = False                                 # Phase 2: Blank Screen
        self.phase4 = False
        self.phase6 = False
        # Reset all events to False
        self.event1 = False
        self.event2 = False
        self.event3 = False

        #random.shuffle(self.icon_position)                              # Randomize the stimuli positions
        self.create_stimuli()                                           # Run the function .create_stimuli()
        #self.start_time = pygame.time.get_ticks()


    def newBlock(self):
        """Moves program to the next block and randomizes the trial types"""
        #pseudorandomize(self.trial_type)                               # WARNING: Do not use if you have only 1 trial type
        self.stimID = -1                                                # Reset stimID to -1 to reloop through stimuli list
        self.block += 1                                                 # Increment block by 1
        random.shuffle(self.stimuli_idx)                                # Reshuffle the stimuli indices
        # Reset all events to False
        self.event1 = False             
        self.event2 = False
        self.event3 = False

        if self.block > self.blocks_per_session:                        # Check if this is the last block in the session
            print("Session Complete!")                                  # If it is, then quit!
            pygame.quit()
            sys.exit()


    def create_stimuli(self):
        """Create the stimuli based on the trial type"""
        """Use choice() to randomly select a stimuli within a range of indices"""
        global icon_condition # Use icon_condition from parameters.txt to counterbalance stimuli between monkeys

        # Create a list called "Icons" that is made up of a list of Objects with the "Icon" Class
        Icons = [Icon("start.png", (150, 200), (140, 140)),
                 Icon("fixation_point.png", (0, 0), (100, 100)),
                 Icon("start.png", (0, 0), (100, 100))]


        # Icons[] determined which pngs are taken in, self.stimuli[] determines which stimuli can be selected for this specific trial
        self.stimuli = [Icons[0], Icons[1], Icons[2]]
        # 0 = Start Button
        # 1 = Leaf
        # 2 = Ram/Uterus
        # 3 = Peach
        # 4 = Peach


# Basic Drawing Functions -------------------------------------------------------------------------------------------------

    def draw_start(self):
        """Draw the start button at center of the screen"""
        self.stimuli[0].mv2pos((400, 75))                                              # The list self.stimuli[] stores the start button at its 0th position
        self.stimuli[0].draw(screen)                                                    # So to reference it, use self.stimuli[0] followed by the function you want to use

    def draw_fixation_point(self):
        """Draw the stimuli at their positions after start button is selected"""
        global icon_positions
        if self.trial_type[self.trial_within_block] == 1:
            self.stimuli[1].mv2pos(self.icon_position[0])
            self.stimuli[1].draw(screen)
        elif self.trial_type[self.trial_within_block] == 2:
            self.stimuli[1].mv2pos(self.icon_position[1])
            self.stimuli[1].draw(screen)
        elif self.trial_type[self.trial_within_block] == 3:
            self.stimuli[1].mv2pos(self.icon_position[2])
            self.stimuli[1].draw(screen)
        elif self.trial_type[self.trial_within_block] == 4:
            self.stimuli[1].mv2pos(self.icon_position[3])
            self.stimuli[1].draw(screen)
        elif self.trial_type[self.trial_within_block] == 5:
            self.stimuli[1].mv2pos(self.icon_position[4])
            self.stimuli[1].draw(screen)


# Time Keeping Funcitons -------------------------------------------------------------------------------------------------

    def get_trial_type(self):
        return self.trial_type[self.trial_within_block]
        print("Trial Type: " + str(self.trial_type[self.trial_within_block]))

    def pre_trial_delay(self):
        """Present a blank screen for standardized 2 sec prior to the presentation of all 4 choice options"""
        if self.time_delay()- self.total_delay >= 2:
            cursor.mv2pos((400, 300))
            self.phase5 = False
            self.phase6 = True

    def time_delay(self):
        """This function counts up time (0.000s) since the start button was touched"""
        delay_counter = ((pygame.time.get_ticks() - self.start_time)/1000)
        print(delay_counter)
        return delay_counter

    def trial_duration(self):
        global timer
        global start_time
        global SELECT
        global duration
        seconds = 0
        if seconds < duration:
            seconds = ((pygame.time.get_ticks() - start_time) / 1000)
            #print(seconds)
        if seconds > duration and SELECT != -1:
            seconds = seconds
        elif seconds > duration and SELECT == -1:
            #sound(False)
            start_time = pygame.time.get_ticks()
            self.trial_number -= 1
            self.trial_within_block -= 1
            self.stimID -= 1
            seconds = 0
            selection = 0
            self.startphase = True
            self.new()

        return seconds

    def response_time(self):
        seconds = 0.000
        if seconds < duration:
            seconds = ((pygame.time.get_ticks() - start_time) / 1000.000)

        return seconds
        
    
# Start the trial! Now its time to start each trial and move through each phase -----------------------------------------------
    def start(self):
        global SELECT
        global timer
        global start_time

        self.draw_start()
        cursor.draw(screen)
        moveCursor(cursor, only = 'up')

        if cursor.collides_with(self.stimuli[0]):                                       # If the cursor collides with the start button
            screen.fill(white)
            cursor.mv2pos((400, 50))
            self.start_time = pygame.time.get_ticks()                                   # Initialize the self.start_time variable
            self.startphase = False                                                     # Cause startphase to become False
            self.phase1 = True                                                          # Cause phase1 to become True


# Phase 1: 6 Second delay, during which either a video [Social Trials], an object gif [Inanimate Trials], or nothing [Filler trials] will play
    def guiding_phase(self):
        """Draw the target at the center of the screen"""
        screen.fill(white)
        self.draw_fixation_point()

        # Start recording only once
        if not self.recording:
            self.et_start_time = time.time()
            eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)
            self.recording = True

        # Stop after 3 seconds
        elapsed_time = time.time() - self.et_start_time
        if elapsed_time >= 3:
            eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)
            self.phase1 = False
            self.phase2 = True
            self.recording = False  # reset if you plan to re-enter this phase

# Phase 2: Run Selection Phase
    def run_trial(self):
        global SELECT
        global timer
        global start_time
        global button_positions
        global duration
        self.draw_fixation_point()
        cursor.draw(screen)
        moveCursor(cursor)
        if cursor.collides_with_list(self.stimuli) == 1:
            print("Collision with stimuli 1")
            self.total_trials += 1
            with open("trial_count_total.txt", "w") as d:
                d.write(str(self.total_trials))
            sound(True)
            pellet()
            screen.fill(white)
            refresh(screen)
            self.phase2 = False
            pygame.time.delay(ITI * 1000)
            self.new()
        

    def write(self, file, side, correct):
        global icon_condition
        now = time.strftime('%H:%M:%S')
        if self.trial_type[self.trial_within_block] <= 4:
            trial_type_cat = "motivation"
        elif self.trial_type[self.trial_within_block] == 5 or self.trial_type[self.trial_within_block] == 6:
            trial_type_cat = "social"
        elif self.trial_type[self.trial_within_block] == 7 or self.trial_type[self.trial_within_block] == 8:
            trial_type_cat = "asocial_object"
        elif self.trial_type[self.trial_within_block] == 9 or self.trial_type[self.trial_within_block] == 10:
            trial_type_cat = "asocial_eyes"
            
        if self.pre_test == True:
            data = [self.total_trials, monkey, today, now, self.pre_test, self.trial_number, self.trial_type[self.trial_within_block], trial_type_cat,
                    self.video_playtime, self.which_video, side, correct]
        elif self.pre_test == False:
            data = [self.total_trials, monkey, today, now, self.pre_test, self.trial_number, self.trial_type[self.trial_within_block], trial_type_cat,
                    self.video_playtime, self.which_video, side, correct]
        
        writeLn(file, data)



# ---------------------------------------------------------------------------------------------------------------------


# UPLOAD TASK PARAMETERS ----------------------------------------------------------------------------------------------
varNames = ['full_screen', 'train_or_test', 'icon_condition', 'trials_per_block', 'blocks_per_session', 'ITI',
            'duration', 'run_time', 'time_out']
params = getParams(varNames)
globals().update(params)

full_screen = params['full_screen']                     # Since your parameters are stored in a dictionary
train_or_test = params['train_or_test']                       # You can pull their value out with dictionary[key]
icon_condition = params['icon_condition']
trials_per_block = params['trials_per_block']
blocks_per_session = params['blocks_per_session']
ITI = params['ITI']
duration = params['duration']
run_time = params['run_time']
time_out = params['time_out']


# START THE CLOCK
clock = pygame.time.Clock()
start_time = (pygame.time.get_ticks() / 1000)
stop_after = run_time * 60 * 1000

# CREATE THE TASK WINDOW
os.environ['SDL_VIDEO_FULLSCREEN_DISPLAY'] = '0'
screen = pygame.display.set_mode(scrSize, pygame.FULLSCREEN)
pygame.display.set_caption("You better look, Bitch - N - NF")
display_icon = pygame.image.load("Monkey_Icon.png")
pygame.display.set_icon(display_icon)
screen.fill(white)

# DEFINE THE CURSOR
cursor = Box(color = red, speed = 10, circle = True)


"""CREATE THE DATA FILE-------------------------------------------------------------------------------------------"""
data_file = makeFileName('Gaze_v2')
eye_data_file = makeFileName('Eye_Data')
writeLn(data_file, ['total_trial_number', 'monkey', 'date', 'time', 'pre_test', 'trial_number', 'trial_type', 'trial_type_cat', 'video_ms', 'video_id', 'side_selected', 'correct_or_incorrect'])
writeLn(eye_data_file, ['total_trial_number', 'monkey', 'date', 'trial', 'trial_type', 'video_ms', 'video_id', 'guiding', 'selection', 'time', 'left_x', 'left_y', 'right_x', 'right_y'])


"""SET UP IS COMPLETE - EVERYTHING BELOW THIS IS RUNNING THE MAIN PROGRAM"""


"""MAIN GAME LOOP -------------------------------------------------------------------------------------------"""
trial = Trial()             # Initialize a new Trial

trial.new()                 # Have the newly initialized trial run .new() function to begin ;)

running = True
while running:
    quitEscQ()
    timer = (pygame.time.get_ticks() / 1000)
    if timer > run_time:
        pygame.quit()
        sys.exit()
    screen.fill(white)
    cursor.draw(screen)
    
    SELECT = cursor.collides_with_list(trial.stimuli)   # While the program is running, the variable called "SELECT"
    clock.tick(fps)                                             # is equal to the number of the stimuli in stimuli[]
    
    if trial.startphase == True:
        trial.start()
    elif trial.startphase == False:
        if trial.phase1 == True:
            trial.guiding_phase()
        elif trial.phase2 == True:
            trial.run_trial()





    refresh(screen)

# --------------------------------------------------------------------------------------------------------------------

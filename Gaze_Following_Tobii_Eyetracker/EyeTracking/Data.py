import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

screensize = (1920, 1080)

os.chdir(r'C:/Users/matth/anaconda3/envs/btg/btg2024/EyeTracking/Files')

Fixations = pd.read_csv('Files\\DATA\\i2mc_output\\Adult1\\Adult1.csv')

raw_data = pd.read_csv('Files\\DATA\\RAW\\Adult1.csv')

dimensions_of_AOI = 600/2
target_position = 500 #The position of the target relative to center

# Area of Interest --------------------------------------------------------------------------------

AOI1 = [[screensize[0]/2 - target_position - dimensions_of_AOI, screensize[1]/2 - dimensions_of_AOI],
        [screensize[0]/2 - target_position + dimensions_of_AOI, screensize[1]/2 + dimensions_of_AOI]]

AOI2 = [[screensize[0]/2 + target_position - dimensions_of_AOI, screensize[1]/2 - dimensions_of_AOI],
        [screensize[0]/2 + target_position + dimensions_of_AOI, screensize[1]/2 + dimensions_of_AOI]]

AOIs = [AOI1, AOI2]

def find_area_for_point(point, areas):

    for i, area in enumerate(areas):
        # Extract bottom left and top right points
        bottom_left, top_right = area
        
        # Extract the x and y of each point
        bottom_x, bottom_y = bottom_left
        top_x, top_y = top_right
        
        # Extract the x and y of our point of interest
        x, y = point
        
        # Check if the point is in the area
        if bottom_x <= x <= top_x and bottom_y <= y <= top_y :
            return(i)
    return(-1)


Targets = raw_data.loc[(raw_data['Event'] == 'Reward') | (raw_data['Event'] == 'NoReward'), ['time', 'Event']].values


# Time of Interest --------------------------------------------------------------------------------
# Having identified the moments when the targets were presented, we can now establish a time window around each of these instances. 
# To accomplish this, we will iterate over the identified times and select all the fixations that occur within the defined window. 
# To make things clearer, we’re going to add two new columns to our fixation dataframe: Event and Event_trial. 
# These will help us know which event each fixation is linked to, and which specific trial it belongs to. 
# Plus, we’re going to add another column called Onset to the fixations dataframe. 
# This will let us store the onset times of specific events, making our analysis down the line a whole lot simpler.

# Find the fixations that we care about
pre  = -750
post = 400

for i,c in enumerate(Targets):
    
    # Find which row meets our conditions
    mask = (Fixations['startT'] >= c[0]+pre) & (Fixations['startT'] < c[0]+post)
    
    # Fill the rows with have found with more info
    Fixations.loc[mask, 'Event'] = c[1]
    Fixations.loc[mask, 'Event_trial'] = i
    Fixations.loc[mask, 'Onset'] =  c[0]

# Filter all the NANs out
Target_fixations = Fixations[Fixations['Event'].notna()].reset_index(drop = True)
#
# Add a column  to our Target_fixations dataframe containing the AOIs we defined together before. 
# Thus, each row of this column will tell us which AOIs we should check. 
# We will also add a new column called Looked_AOI where we will store the indexes of which AOI the fixation fell into.

Target_fixations['AOIs'] = [AOIs]* len(Target_fixations)
Target_fixations['Looked_AOI'] = np.nan

# We run the function  for each row. We pass each xpos and ypos to the function
# toghether with the areas
for row in range(len(Target_fixations)):
    
    Point = Target_fixations.loc[row, ['xpos', 'ypos']].values
    Areas = Target_fixations.loc[row, 'AOIs']
    
    Target_fixations.loc[row, 'Looked_AOI'] = find_area_for_point(Point, Areas)

# Filter for AOI of interest
# Remove all that lay outside the AOI
# 0 is AOI1
# 1 is AOI2
# -1 is outside either AOI
Target_fixations = Target_fixations[Target_fixations['Looked_AOI'] != -1]
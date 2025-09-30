import os
import tobii_research as tr
import pygame

found_eyetrackers = tr.find_all_eyetrackers()

white = (255, 255, 255)

for eyetracker in found_eyetrackers:
    print("Address: " + eyetracker.address)
    print("Model: " + eyetracker.model)
    #print("Serial Number: " + eyetracker.serial_number)

eyetracker = tr.EyeTracker("tet-tcp://169.254.252.248")
print("Successfully connected to: ", eyetracker.serial_number)



os.environ['SDL_VIDEO_FULLSCREEN_DISPLAY'] = '1'

pygame.init()

scrSize = (800, 600)
screen = pygame.display.set_mode(scrSize, pygame.FULLSCREEN)
screen.fill(white)

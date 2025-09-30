import tobii_research as tr
import pygame
import sys

# Initialize Pygame to handle keyboard input
pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Eye Tracker Validity Viewer")

# Find and connect to the eye tracker
eyetrackers = tr.find_all_eyetrackers()
if not eyetrackers:
    print("No eye tracker found.")
    sys.exit()
et = eyetrackers[0]
print("Connected to:", et)

# --- Calibration ---
calibration = tr.ScreenBasedCalibration(et)
calibration.enter_calibration_mode()

print("Show the first point (center). Press Enter when participant is looking...")
input()
calibration.collect_data(0.5, 0.5)

print("Show the second point (right). Press Enter when participant is looking...")
input()
calibration.collect_data(0.9, 0.5)

result = calibration.compute_and_apply()
print("Calibration status:", result.status)
calibration.leave_calibration_mode()

# --- Gaze Data Callback ---
gaze_data_latest = {}

def store_gaze_data(data):
    global gaze_data_latest
    gaze_data_latest = data

# Subscribe to gaze data
et.subscribe_to(tr.EYETRACKER_GAZE_DATA, store_gaze_data, as_dictionary=True)

print("Press SPACE to print validity and gaze data. Press ESC or close window to exit.")

# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE:
                screen_width = 1440
                screen_height = 900

                left = gaze_data_latest.get('left_gaze_point_on_display_area')
                right = gaze_data_latest.get('right_gaze_point_on_display_area')
                left_valid = gaze_data_latest.get('left_gaze_point_validity')
                right_valid = gaze_data_latest.get('right_gaze_point_validity')

                if left:
                    left_x = int(left[0] * screen_width)
                    left_y = int(left[1] * screen_height)
                else:
                    left_x, left_y = None, None

                if right:
                    right_x = int(right[0] * screen_width)
                    right_y = int(right[1] * screen_height)
                else:
                    right_x, right_y = None, None

                print(f"Left: ({left_x}, {left_y}), Validity: {left_valid}")
                print(f"Right: ({right_x}, {right_y}), Validity: {right_valid}")

# --- Cleanup ---
et.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, store_gaze_data)
pygame.quit()
sys.exit()

import tobii_research as tr

# Find connected eye trackers
eyetrackers = tr.find_all_eyetrackers()

if not eyetrackers:
    print("No eye tracker found.")
    exit()

et = eyetrackers[0]
print("Connected to:", et)

# Simple gaze data printer
def print_gaze(data):
    print("Left:", data['left_gaze_point_on_display_area'],
          "Validity:", data['left_gaze_point_validity'])

# Subscribe to gaze data stream
et.subscribe_to(tr.EYETRACKER_GAZE_DATA, print_gaze, as_dictionary=True)

input("Press Enter to stop...")

# Unsubscribe and clean up
et.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, print_gaze)

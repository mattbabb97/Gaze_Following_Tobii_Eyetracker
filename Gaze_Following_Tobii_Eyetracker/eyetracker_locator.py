import clr
import sys
import os

# === STEP 1: Add reference to Tobii Analytics SDK ===
dll_path = r"C:\Path\To\Tobii.EyeTracking.IO.dll"  # <-- UPDATE THIS PATH
if not os.path.exists(dll_path):
    raise FileNotFoundError("Could not find Tobii.EyeTracking.IO.dll at specified path.")

 

clr.AddReference(dll_path)

# === STEP 2: Import the required .NET namespaces ===
from Tobii.EyeTracking.IO import EyeTrackerCollection, EyeTracker

# === STEP 3: Initialize the eye tracker collection ===
trackers = EyeTrackerCollection.Instance

 

if trackers.Count == 0:
    print("No eye trackers found.")
else:
    for tracker in trackers:
        print("=== Eye Tracker Info ===")
        print("Address      :", tracker.Address)
        print("Model        :", tracker.Model)
        print("Name         :", tracker.Name)
        print("SerialNumber :", tracker.SerialNumber)
        print("========================\n")

        # Example: Connect to the first tracker
        connected_tracker = EyeTracker.CreateEyeTracker(tracker.Address)
        print("Connected to:", connected_tracker.Name)


 

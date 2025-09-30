import tobii_research as tr

et = tr.find_all_eyetrackers()[0]

calibration = tr.ScreenBasedCalibration(et)
calibration.enter_calibration_mode()

print("Show the first point (center). Press Enter when participant is looking...")
input()
calibration.collect_data(0.5, 0.5)

print("Show second point (right). Press Enter when participant is looking...")
input()
calibration.collect_data(0.9, 0.5)

result = calibration.compute_and_apply()
print("Calibration status:", result.status)

calibration.leave_calibration_mode()

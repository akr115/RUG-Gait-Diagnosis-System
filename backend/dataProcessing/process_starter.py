from .c3d_reader import readC3D, trimGlobals, readXLSX
from .comparer import compareJointAngles
from .diagnoser import diagnose
import os

def process(threshold, directory_c3d, directory_xlsx):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_normal = './Walk_100_03.c3d'
    # Read the xlsx file
    lo = readXLSX(directory_xlsx)
    print("Trying to read the global events of the normal gait")
    # Read the c3d file of normal gait
    global_events_normal, LAnglesNormal, RAnglesNormal, first_frame_normal, frame_rate_normal = (
        readC3D(os.path.join(base_dir, file_path_normal)))
    print("Trying to read the global events of the patient")
    # Read the c3d file of the patient
    global_events, LAngles, RAngles, first_frame, frame_rate = readC3D(directory_c3d)
    # Trim the global events for both gaits
    global_events = trimGlobals(global_events)
    global_events_normal=trimGlobals(global_events_normal)
    # Compare the joint angles of the patient with the normal gait
    joint_angles_differences = compareJointAngles(global_events, global_events_normal, LAngles, RAngles, LAnglesNormal,
                                                  RAnglesNormal,first_frame_normal, first_frame, frame_rate_normal,
                                                  frame_rate, threshold)
    variable_names = lo["Variable"].tolist()
    variable_values = lo["Value"].tolist()
    # Diagnose the patient
    diagnosis, lo = diagnose(joint_angles_differences, variable_names, variable_values)

    # Return the diagnosis and list of relevant LO variables
    return diagnosis, lo

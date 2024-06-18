from c3d_reader import readC3D, trimGlobals, readXLSX
from comparer import compareJointAngles
from diagnoser import diagnose
import pandas as pd

if __name__ == "__main__":
    file_path_normal = '/Users/amoor/Downloads/Walk_100_03.c3d'
    file_path = '/Users/amoor/Downloads/WalkNormal01.c3d'
    lo_file_path = '/Users/amoor/Downloads/LO.xlsx'
    lo = readXLSX(lo_file_path)
    global_events_normal, LAnglesNormal, RAnglesNormal, first_frame_normal, last_frame_normal, frame_rate_normal = (
        readC3D(file_path_normal))
    global_events, LAngles, RAngles, first_frame, last_frame, frame_rate = readC3D(file_path)
    global_events = trimGlobals(global_events)
    global_events_normal=trimGlobals(global_events_normal)
    joint_angles_differences = compareJointAngles(global_events, global_events_normal, LAngles, RAngles, LAnglesNormal, RAnglesNormal,
                       first_frame_normal, last_frame_normal, first_frame, last_frame, frame_rate_normal, frame_rate)
    variable_names = lo["Variable"].tolist()
    variable_values = lo["Value"].tolist()
    print(len(variable_names))
    print(len(variable_values))
    diagnosis = diagnose(joint_angles_differences, variable_names, variable_values)
    print(diagnosis)


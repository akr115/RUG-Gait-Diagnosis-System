import numpy as np
import pandas as pd
import pyc3dtools

ground_level = 0.05
def detect_gait_stages(data, ground_level=0.05, threshold=0.05):
    gait_stages = {'initial_contact': [], 'flat_foot': [], 'mid_stance': [], 'heel_off': [], 'toe_off': []}

    for i in range(1, len(data)):
        if is_initial_contact(data.iloc[i], data.iloc[i - 1], ground_level):
            gait_stages['initial_contact'].append(i)
        if is_flat_foot(data.iloc[i], ground_level):
            gait_stages['flat_foot'].append(i)
        if is_mid_stance(data.iloc[i], threshold):
            gait_stages['mid_stance'].append(i)
        if is_heel_off(data.iloc[i], data.iloc[i - 1], ground_level):
            gait_stages['heel_off'].append(i)
        if is_toe_off(data.iloc[i], data.iloc[i - 1], ground_level):
            gait_stages['toe_off'].append(i)

    return gait_stages


def is_initial_contact(current_frame, previous_frame, ground_level):
    return previous_frame['RHEE'] > ground_level and current_frame['RHEE'] <= ground_level


def is_flat_foot(current_frame, ground_level):
    return current_frame['RHEE'] <= ground_level and current_frame['RTOE'] <= ground_level


def is_mid_stance(current_frame, threshold):
    return is_flat_foot(current_frame, ground_level) and abs(current_frame['RTHI'] - current_frame['RANK']) < threshold


def is_heel_off(current_frame, previous_frame, ground_level):
    return previous_frame['RHEE'] <= ground_level and current_frame['RHEE'] > ground_level and current_frame[
        'RTOE'] <= ground_level


def is_toe_off(current_frame, previous_frame, ground_level):
    return previous_frame['RTOE'] <= ground_level and current_frame['RTOE'] > ground_level


# Load the C3D file
c3d_file = "/Users/amoor/Downloads/WalkNormal01.c3d"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2M2VlNDFlY2RmODE2MDk0MTI0ZTEyNjIiLCJpYXQiOjE2ODc0MDk1ODEsImV4cCI6MTY4NzQxMzE4MX0.KwuGt4MNbuR2QcwMy4clRB8waVy0anBcdmDDyCF3y3c"
c3d = pyc3dtools.readC3D(TOKEN, c3d_file)

# Extract labels
labels = c3d['Markers Label']

# Extract the 3D marker positions (Z-coordinates only)
First_Frame = c3d['Header']['first_frame']
Last_Frame = c3d['Header']['last_frame']

num_frames = Last_Frame - First_Frame

marker_data = {label: c3d.get_marker_data(label)[:, 2] for label in labels}

# Create a dataframe for the Z-coordinates of markers
df = pd.DataFrame(marker_data)

# Detect gait stages
gait_stages = detect_gait_stages(df)

# Display the gait stages
print(gait_stages)
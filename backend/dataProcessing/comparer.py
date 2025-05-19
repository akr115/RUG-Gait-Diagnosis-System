import numpy as np
import pandas as pd
# Calculates the indices for both gait cycles (normal and undiagnosed) for the same event
def calculateIndices(event, event_normal, frame_rate_normal, frame_rate, first_frame_normal, first_frame):
    index_frame_normal = int(frame_rate_normal * event_normal['times']) - first_frame_normal
    index_frame = int(frame_rate * event['times']) - first_frame
    return index_frame_normal, index_frame
# Calculate the differences between the joint angles and the normal joint angles
def calculateDifferences(ankleAngles, kneeAngles, hipAngles , ankleAnglesNormal,  kneeAnglesNormal, hipAnglesNormal,
                         frameNormal, frame, threshold):

    diff_array = []
    result = []
    # Extract the angles and append the differences to the list
    angles=[hipAngles[frame], kneeAngles[frame], ankleAngles[frame]]
    diff_array.append(hipAngles[frame] - hipAnglesNormal[frameNormal])
    diff_array.append(kneeAngles[frame] - kneeAnglesNormal[frameNormal])
    diff_array.append(ankleAngles[frame] - ankleAnglesNormal[frameNormal])
    # Compare the differences with the threshold value
    for i in range(0, len(diff_array)):
        if diff_array[i] <= -threshold:
            result.append(-1)
        elif diff_array[i] >= threshold:
            result.append(1)
        else:
            result.append(0)

    return result, angles
# Compares the joint angles with the normal joint angles
def compareJointAngles(global_events, global_events_normal, LAngles, RAngles, LAnglesNormal, RAnglesNormal,
                       first_frame_normal, first_frame, frame_rate_normal, frame_rate, threshold):
    hip_index = 0
    knee_index = 1
    ankle_index = 2

    data_labels = ["LHip","LHip Degrees", "LKnee", "LKnee Degrees" ,"LAnkle", "LAnkle Degrees" ,"RHip","RHip Degrees",
                   "RKnee", "RKnee Degrees", "RAnkle", "RAnkle Degrees", "Foot", "Event"]
    data = []

    # Extract  joint angles for the left leg
    LAnkleAngles = LAngles[ankle_index][:, 0]
    LKneeAngles = LAngles[knee_index][:, 0]
    LHipAngles = LAngles[hip_index][:, 0]
    LAnkleAnglesNormal = LAnglesNormal[ankle_index][:, 0]
    LKneeAnglesNormal = LAnglesNormal[knee_index][:, 0]
    LHipAnglesNormal = LAnglesNormal[hip_index][:, 0]

    # Extract joint angles for the right leg
    RAnkleAngles = RAngles[ankle_index][:, 0]
    RKneeAngles = RAngles[knee_index][:, 0]
    RHipAngles = RAngles[hip_index][:, 0]
    RAnkleAnglesNormal = RAnglesNormal[ankle_index][:, 0]
    RKneeAnglesNormal = RAnglesNormal[knee_index][:, 0]
    RHipAnglesNormal = RAnglesNormal[hip_index][:, 0]

    for index, global_event in global_events.iterrows():

        # Find the same event in the normal global_events
        global_event_normal = global_events_normal.loc[
            (global_events_normal['foot'] == global_event['foot']) &
            (global_events_normal['labels'] == global_event['labels'])].iloc[0] # <- take the first occurrence
        index_frame_normal, index_frame = calculateIndices(global_event, global_event_normal, frame_rate_normal,
                                                           frame_rate, first_frame_normal, first_frame)

        # Call calculateDifferences for the left foot
        result_l, angles_l = calculateDifferences(LAnkleAngles, LKneeAngles, LHipAngles, LAnkleAnglesNormal,
                                                  LKneeAnglesNormal, LHipAnglesNormal, index_frame_normal, index_frame,
                                                  threshold)
        # Call calculateDifferences for the right foot
        result_r, angles_r = calculateDifferences(RAnkleAngles, RKneeAngles, RHipAngles, RAnkleAnglesNormal,
                                                  RKneeAnglesNormal, RHipAnglesNormal, index_frame_normal, index_frame,
                                                  threshold)
        # Append the results to the data list
        data.append([result_l[0], angles_l[0], result_l[1], angles_l[1], result_l[2], angles_l[2],
                     result_r[0], angles_r[0], result_r[1], angles_r[1], result_r[2], angles_r[2],
                     global_event['foot'], global_event['labels']])
    # Convert the list into a DataFrame and return it
    df = pd.DataFrame(data, columns=data_labels)
    return df






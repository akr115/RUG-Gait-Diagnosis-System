import numpy as np
import pandas as pd

def calculateIndices(event, event_normal, frame_rate_normal, frame_rate, first_frame_normal, first_frame):
    index_frame_normal = int(frame_rate_normal * event_normal['times']) - first_frame_normal
    index_frame = int(frame_rate * event['times']) - first_frame
    return index_frame_normal, index_frame

def calculateDifferences(ankleAngles, kneeAngles, hipAngles , ankleAnglesNormal,  kneeAnglesNormal, hipAnglesNormal, frameNormal, frame):
    diff_array = []
    result = []
    diff_array.append(hipAngles[frame] - hipAnglesNormal[frameNormal])
    diff_array.append(kneeAngles[frame] - kneeAnglesNormal[frameNormal])
    diff_array.append(ankleAngles[frame] - ankleAnglesNormal[frameNormal])

    for i in range(0, len(diff_array)):
        if diff_array[i] <= -8:
            result.append(-1)
        elif diff_array[i] >= 8:
            result.append(1)
        else:
            result.append(0)

    return result

def compareJointAngles(global_events, global_events_normal, LAngles, RAngles, LAnglesNormal, RAnglesNormal,
                       first_frame_normal, last_frame_normal, first_frame, last_frame, frame_rate_normal, frame_rate):
    hip_index = 0
    knee_index = 1
    ankle_index = 2

    data_labels = ["LHip", "LKnee", "LAnkle", "RHip", "RKnee", "RAnkle", "Foot", "Event"]
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

        #Find the same event in the normal global_events
        global_event_normal = global_events_normal.loc[
            (global_events_normal['foot'] == global_event['foot']) &
            (global_events_normal['labels'] == global_event['labels'])].iloc[0] # <- take the first occurrence
        index_frame_normal, index_frame = calculateIndices(global_event, global_event_normal, frame_rate_normal,
                                                           frame_rate, first_frame_normal, first_frame)

        #Call calculateDifferences for the left foot
        result_l = calculateDifferences(LAnkleAngles, LKneeAngles, LHipAngles, LAnkleAnglesNormal, LKneeAnglesNormal, LHipAnglesNormal, index_frame_normal, index_frame)
        #Call calculateDifferences for the right foot
        result_r = calculateDifferences(RAnkleAngles, RKneeAngles, RHipAngles, RAnkleAnglesNormal, RKneeAnglesNormal, RHipAnglesNormal, index_frame_normal, index_frame)


        data.append([result_l[0], result_l[1], result_l[2], result_r[0], result_r[1], result_r[2], global_event['foot'], global_event['labels']])
    df = pd.DataFrame(data, columns=data_labels)
    return df






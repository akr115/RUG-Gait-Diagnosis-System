import ezc3d
import pandas as pd
import numpy as np




def findMidStance(markersWithLabels, Fs_MarkerPositions, times, contexts, events):
    evnt_ic_right = 1e10
    evnt_ic_left = 1e10
    evnt_footoff_right = -1
    evnt_footoff_left = -1

    LANK = markersWithLabels['LANK']  # L=left; ANK = Ankle marker
    LANK = np.array([list(LANK[elem]) for elem in LANK.keys()])  # asl: turn to numpy
    LKNE = markersWithLabels['LKNE']  # Knee marker
    LKNE = np.array([list(LKNE[elem]) for elem in LKNE.keys()])  # asl: turn to numpy

    RANK = markersWithLabels['RANK']  # L=left; ANK = Ankle marker
    RANK = np.array([list(RANK[elem]) for elem in RANK.keys()])  # asl: turn to numpy
    RKNE = markersWithLabels['RKNE']  # Knee marker
    RKNE = np.array([list(RKNE[elem]) for elem in RKNE.keys()])  # asl: turn to numpy

    # this for loop basically selects the time window in which the mid-stance could happen
    for i in range(0, len(events)):
        if evnt_ic_right == 1e10 and 'Foot Strike' in events[i] and 'Right' in contexts[
            i]:  # select starting point of cycle with right foot strike (foot just touches the floor)
            evnt_ic_right = times[i]
        elif evnt_footoff_right == -1 and 'Foot Off' in events[i] and 'Right' in contexts[i] and times[
            i] > evnt_ic_right:  # select end of timeframe where mid-stance could happen (when right foot starts to leave floor)
            evnt_footoff_right = times[i]
        elif evnt_ic_left == 1e10 and 'Foot Strike' in events[i] and 'Left' in contexts[
            i]:
            evnt_ic_left = times[i]
        elif evnt_footoff_left == -1 and 'Foot Off' in events[i] and 'Left' in contexts[i] and times[
            i] > evnt_ic_left:
            evnt_footoff_left = times[i]

    event_ic_right = int(evnt_ic_right * Fs_MarkerPositions)
    event_footoff_right = int(evnt_footoff_right * Fs_MarkerPositions)
    event_ic_left = int(evnt_ic_left * Fs_MarkerPositions)
    event_footoff_left = int(evnt_footoff_left * Fs_MarkerPositions)

    # For the right foot select the frame where the midstance may occur.
    d1_d2_right = np.abs(np.sqrt(np.square(LKNE[event_ic_right:event_footoff_right, 2] - LANK[event_ic_right:event_footoff_right, 2])) - np.sqrt(
        np.square(RKNE[event_ic_right:event_footoff_right, 2] - LKNE[event_ic_right:event_footoff_right, 2])))
    midStance_right = np.argmin(d1_d2_right) + event_ic_right


    # For the left foot select the frame where the midstance may occur.
    d1_d2_left = np.abs(np.sqrt(np.square(RKNE[event_ic_left:event_footoff_left, 2] - RANK[event_ic_left:event_footoff_left, 2])) - np.sqrt(
        np.square(RKNE[event_ic_left:event_footoff_left, 2] - LKNE[event_ic_left:event_footoff_left, 2])))
    midStance_left = np.argmin(d1_d2_left) + event_ic_left

    return midStance_right, midStance_left

# The terminal stance is computed as an estimation of 10 frames before the opposite foot strikes the ground.
def findTerminalStance(Fs_MarkerPositions, times, contexts, events):
    evnt_footstrike_right = []
    evnt_footstrike_left = []
    evnt_terminalStance_right = []
    evnt_terminalStance_left = []

    # Find all the frames where the foot off event occurs
    for i in range(0, len(events)):
        if 'Foot Strike' in events[i] and 'Right' in contexts[i]:
            evnt_footstrike_right.append(times[i])
        elif 'Foot Strike' in events[i] and 'Left' in contexts[i]:
            evnt_footstrike_left.append(times[i])

    # Find the frames where the terminal stance event occurs
    # We estimate it by 10 frames before the opposite leg has 'Foot Strike'
    for i in range(0, len(evnt_footstrike_right)):
        evnt_terminalStance_left.append(evnt_footstrike_right[i] - 10 / Fs_MarkerPositions)
    for i in range(0, len(evnt_footstrike_left)):
        evnt_terminalStance_right.append(evnt_footstrike_left[i] - 10 / Fs_MarkerPositions)

    return evnt_terminalStance_right, evnt_terminalStance_left


def findLoadingResponse(Fs_MarkerPositions, times, contexts, events):
    evnt_footoff_right = []
    evnt_footoff_left = []
    evnt_loading_resp_right = []
    evnt_loading_resp_left = []
    
    # Find all the frames where the foot off event occurs
    for i in range(0, len(events)):
        if 'Foot Off' in events[i] and 'Right' in contexts[i]:
            evnt_footoff_right.append(times[i])
        elif 'Foot Off' in events[i] and 'Left' in contexts[i]:
            evnt_footoff_left.append(times[i])

    
    # Find the frames where the terminal stance event occurs
    # We estimate it by 10 frames before the opposite leg has 'Foot Off'
    for i in range(0, len(evnt_footoff_right)):
        evnt_loading_resp_right.append(evnt_footoff_left[i] - 10 / Fs_MarkerPositions)
    for i in range(0, len(evnt_footoff_left)):
        evnt_loading_resp_left.append(evnt_footoff_right[i] - 10 / Fs_MarkerPositions)


    return evnt_loading_resp_right, evnt_loading_resp_left

def extractC3D(file_path):
    c3d_file = ezc3d.c3d(file_path)
    labels = c3d_file['parameters']['POINT']['LABELS']['value']
    label_values = c3d_file['data']['points']
    data = {label: {} for label in labels}
    numberOfIndicators = len(c3d_file['data']['points'][0])  # Count of all indicators ('LASI', 'RASI', etc.)
    numberOfFramesPerIndicator = len(c3d_file['data']['points'][0][0])  # Number of frames per indicator
    contexts = c3d_file['parameters']['EVENT']['CONTEXTS']['value']
    contexts_labels = c3d_file['parameters']['EVENT']['LABELS']['value']
    contexts_frames = c3d_file['parameters']['EVENT']['TIMES']['value'][1, :]
    frameRate = c3d_file['header']['points']['frame_rate']

    for i in range(0, numberOfIndicators):
        for j in range(0, numberOfFramesPerIndicator):
            data[labels[i]][j] = []
            for k in range(0, 3):
                data[labels[i]][j].append(label_values[k][i][j])

    df = pd.DataFrame(data)
    d = {'foot': contexts, 'labels': contexts_labels, 'times': contexts_frames}
    globalEvents = pd.DataFrame(d).sort_values('times').reset_index(drop=True)
    midStance_r, midStance_l = findMidStance(data, frameRate, globalEvents['times'], globalEvents['foot'],
                                             globalEvents['labels'])
    terminalStance_r, terminalStance_l = findTerminalStance(frameRate, globalEvents['times'], globalEvents['foot'], globalEvents['labels'])
    terminalStance = pd.DataFrame({
        'foot': ['Right'] * len(terminalStance_r) + ['Left'] * len(terminalStance_l),
        'labels': ['Terminal Stance'] * (len(terminalStance_r) + len(terminalStance_l)),
        'times': [time for time in terminalStance_r] + [time  for time in terminalStance_l]
    })

    loadingResponse_r, loadingResponse_l = findLoadingResponse(frameRate, globalEvents['times'], globalEvents['foot'], globalEvents['labels'])
    loadingResponse = pd.DataFrame({
        'foot': ['Right'] * len(loadingResponse_r) + ['Left'] * len(loadingResponse_l),
        'labels': ['Loading Response'] * (len(loadingResponse_r) + len(loadingResponse_l)),
        'times': [time for time in loadingResponse_r] + [time for time in loadingResponse_l]
    })
    midStance = {'foot': ['Right', 'Left'], 'labels': ['Mid Stance', 'Mid Stance'], 'times': [int(midStance_r)/frameRate, int(midStance_l)/frameRate]}
    midStanceDF = pd.DataFrame(midStance)
    globalEvents = pd.concat([globalEvents, midStanceDF], ignore_index=True)
    globalEvents = pd.concat([globalEvents, terminalStance], ignore_index=True)
    globalEvents = pd.concat([globalEvents, loadingResponse], ignore_index=True)
    globalEvents = globalEvents.sort_values('times').reset_index(drop=True)
    return globalEvents

def trimGlobals(globalEvents):
    midStanceCounter = 0
    footStrikeCounter = 0
    loadingResponseCounter = 0
    footOffCounter = 0
    terminalStanceCounter = 0
    firstIndex = 0
    lastIndex = -1

    for i, row in globalEvents.iterrows():

        if row['labels'] == "Foot Strike":
            footStrikeCounter += 1
        elif row['labels'] == "Mid Stance":
            midStanceCounter += 1
        elif row['labels'] == "Foot Off":
            footOffCounter += 1
        elif row['labels'] == "Loading Response":
            loadingResponseCounter += 1
        elif row['labels'] == "Terminal Stance":
            terminalStanceCounter += 1
        if footStrikeCounter >= 2 and midStanceCounter >= 2 and footOffCounter >= 2 and loadingResponseCounter >= 2 and terminalStanceCounter >= 2:
            lastIndex = i
            break



    # Slice the DataFrame up to the current index
    filtered_globalEvents = globalEvents.iloc[firstIndex: lastIndex + 1]
    return filtered_globalEvents

if __name__ == "__main__":
    file_path_normal = '/Users/amoor/Downloads/Walk_100_03.c3d'
    file_path = '/Users/amoor/Downloads/WalkNormal01.c3d'
    global_events_normal = extractC3D(file_path_normal)
    global_events = extractC3D(file_path)
    global_events = trimGlobals(global_events)
    global_events_normal=trimGlobals(global_events_normal)

    print(global_events_normal)
    print("-----------------------------------")
    print(global_events)








import numpy as np

# This function estimates the midstance. This is done by extracting the marker positions for the left ankle,
# the left knee, the right ankle and the right knee.
# Given the distance d1 between the left knee and the left ankle,
# and the horizontal distance d2 between the right knee and the left knee,
# the distances with the least difference d1-d2 is found, yielding the mid-stance for the right leg.
# The left leg's midstance is also estimated the same way,
# with the only difference being we use the right ankle and right knee for d1.
#  The midstance is estimated by finding the frame where the difference between the distances d1 and d2 is the smallest.
def findMidStance(markersWithLabels, Fs_MarkerPositions, times, contexts, events):
    evnt_ic_right = 1e10
    evnt_ic_left = 1e10
    evnt_footoff_right = -1
    evnt_footoff_left = -1

    LANK = markersWithLabels['LANK']  # L=left; ANK = Ankle marker
    LANK = np.array([list(LANK[elem]) for elem in LANK.keys()])  # Turn to numpy
    LKNE = markersWithLabels['LKNE']  # Knee marker
    LKNE = np.array([list(LKNE[elem]) for elem in LKNE.keys()])  # Turn to numpy

    RANK = markersWithLabels['RANK']  # L=left; ANK = Ankle marker
    RANK = np.array([list(RANK[elem]) for elem in RANK.keys()])  # Turn to numpy
    RKNE = markersWithLabels['RKNE']  # Knee marker
    RKNE = np.array([list(RKNE[elem]) for elem in RKNE.keys()])  # Turn to numpy

    # Select the frames where the foot strike and foot off events occur such that the mid-stance can be estimated
    for i in range(0, len(events)):
        if evnt_ic_right == 1e10 and 'Foot Strike' in events[i] and 'Right' in contexts[
            i]:  # select starting point of cycle with right foot strike (foot just touches the floor)
            evnt_ic_right = times[i]
        elif evnt_footoff_right == -1 and 'Foot Off' in events[i] and 'Right' in contexts[i] and times[
            i] > evnt_ic_right:  # select end of timeframe where mid-stance could happen (when right foot starts to leave floor)
            evnt_footoff_right = times[i]
        elif evnt_ic_left == 1e10 and 'Foot Strike' in events[i] and 'Left' in contexts[
            i]:
            evnt_ic_left = times[
                i]  # select starting point of cycle with left foot strike (foot just touches the floor)
        elif evnt_footoff_left == -1 and 'Foot Off' in events[i] and 'Left' in contexts[i] and times[
            i] > evnt_ic_left:
            evnt_footoff_left = times[
                i]  # select end of timeframe where mid-stance could happen (when left foot starts to leave floor)

    event_ic_right = int(evnt_ic_right * Fs_MarkerPositions)
    event_footoff_right = int(evnt_footoff_right * Fs_MarkerPositions)
    event_ic_left = int(evnt_ic_left * Fs_MarkerPositions)
    event_footoff_left = int(evnt_footoff_left * Fs_MarkerPositions)

    # For the right foot select the frame where the midstance may occur.
    d1_d2_right = np.abs(np.sqrt(
        np.square(LKNE[event_ic_right:event_footoff_right, 2] - LANK[event_ic_right:event_footoff_right, 2])) - np.sqrt(
        np.square(RKNE[event_ic_right:event_footoff_right, 2] - LKNE[event_ic_right:event_footoff_right, 2])))
    midStance_right = np.argmin(d1_d2_right) + event_ic_right

    # For the left foot select the frame where the midstance may occur.
    d1_d2_left = np.abs(np.sqrt(
        np.square(RKNE[event_ic_left:event_footoff_left, 2] - RANK[event_ic_left:event_footoff_left, 2])) - np.sqrt(
        np.square(RKNE[event_ic_left:event_footoff_left, 2] - LKNE[event_ic_left:event_footoff_left, 2])))
    midStance_left = np.argmin(d1_d2_left) + event_ic_left

    return midStance_right, midStance_left


# The terminal stance is computed as an estimation of 10 frames before the opposite foot strikes the ground.
def findTerminalStance(Fs_MarkerPositions, times, contexts, events):
    evnt_footstrike_right = []
    evnt_footstrike_left = []
    evnt_terminalStance_right = []
    evnt_terminalStance_left = []
    frame_estimation = 10

    # Find all the frames where the foot off event occurs
    for i in range(0, len(events)):
        if 'Foot Strike' in events[i] and 'Right' in contexts[i]:
            evnt_footstrike_right.append(times[i])
        elif 'Foot Strike' in events[i] and 'Left' in contexts[i]:
            evnt_footstrike_left.append(times[i])

    # Find the frames where the terminal stance event occurs
    # We estimate it by 10 frames before the opposite leg has 'Foot Strike'
    for i in range(0, len(evnt_footstrike_right)):
        evnt_terminalStance_left.append(evnt_footstrike_right[i] - frame_estimation / Fs_MarkerPositions)
    for i in range(0, len(evnt_footstrike_left)):
        evnt_terminalStance_right.append(evnt_footstrike_left[i] - frame_estimation / Fs_MarkerPositions)

    return evnt_terminalStance_right, evnt_terminalStance_left


# The loading response is computed as an estimation of 10 frames before the opposite foot leaves the ground.
def findLoadingResponse(Fs_MarkerPositions, times, contexts, events):
    evnt_footoff_right = []
    evnt_footoff_left = []
    evnt_loading_resp_right = []
    evnt_loading_resp_left = []
    frame_estimation = 10

    # Find all the frames where the foot off event occurs
    for i in range(0, len(events)):
        if 'Foot Off' in events[i] and 'Right' in contexts[i]:
            evnt_footoff_right.append(times[i])
        elif 'Foot Off' in events[i] and 'Left' in contexts[i]:
            evnt_footoff_left.append(times[i])

    # Find the frames where the terminal stance event occurs
    # We estimate it by 10 frames before the opposite leg has 'Foot Off'
    for i in range(0, len(evnt_footoff_left)):
        evnt_loading_resp_right.append(evnt_footoff_left[i] - frame_estimation / Fs_MarkerPositions)
    for i in range(0, len(evnt_footoff_right)):
        evnt_loading_resp_left.append(evnt_footoff_right[i] - frame_estimation / Fs_MarkerPositions)

    return evnt_loading_resp_right, evnt_loading_resp_left
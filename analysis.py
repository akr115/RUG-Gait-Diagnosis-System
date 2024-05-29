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
    # print(event_ic_right)
    # print(event_footoff_right)
    # print(event_ic_left)
    # print(event_footoff_left)

    # For the right foot select the frame where the midstance may occur.
    d1_d2_right = np.abs(np.sqrt(np.square(LKNE[event_ic_right:event_footoff_right, 2] - LANK[event_ic_right:event_footoff_right, 2])) - np.sqrt(
        np.square(RKNE[event_ic_right:event_footoff_right, 2] - LKNE[event_ic_right:event_footoff_right, 2])))
    midStance_right = np.argmin(d1_d2_right) + event_ic_right
    print(midStance_right)

    # For the left foot select the frame where the midstance may occur.
    d1_d2_left = np.abs(np.sqrt(np.square(RKNE[event_ic_left:event_footoff_left, 2] - RANK[event_ic_left:event_footoff_left, 2])) - np.sqrt(
        np.square(RKNE[event_ic_left:event_footoff_left, 2] - LKNE[event_ic_left:event_footoff_left, 2])))
    midStance_left = np.argmin(d1_d2_left) + event_ic_left
    print(midStance_left)

    # event_ic = int(evnt_ic * Fs_MarkerPositions)
    # event_footoff = int(evnt_footoff * Fs_MarkerPositions)
    #
    # # select frames in which distances between left ankle and right ankle , left knee and right knee. This only considers horizontal distance (so does not consider 3d vectors, but only the Z coordinate)
    # RKNE_LANK = np.abs(np.sqrt(np.square(RANK[event_ic:event_footoff, 2] - LANK[event_ic:event_footoff, 2])) - np.sqrt(
    #     np.square(RKNE[event_ic:event_footoff, 2] - LKNE[event_ic:event_footoff, 2])))
    #
    # # extract exact frame at which the mid-stance event occurrs.
    # midStance = np.argmin(RKNE_LANK) + event_ic
    # print(midStance)

    # # COMPUTE DISTANCES FOR ALL FRAMES AND PLOT WHERE EXACTLY IS THE COMPUTED MID-STANCE SUPPOSED TO BE HAPPENING (for validation purposes)
    # RKNE_LANK_ALL = np.abs(np.sqrt(np.square(RANK[:, 2] - LANK[:, 2])) - np.sqrt(np.square(RKNE[:, 2] - LKNE[:, 2])))
    # plt.plot(np.arange(len(RKNE_LANK_ALL)), RKNE_LANK_ALL)
    # plt.axvline(midStance, color='r')
    # plt.show()

    return midStance_right, midStance_left


if __name__ == "__main__":
    file_path = '/Users/amoor/Downloads/Walk_100_03.c3d'
    c3d_file = ezc3d.c3d(file_path)
    labels = c3d_file['parameters']['POINT']['LABELS']['value']
    label_values = c3d_file['data']['points']
    data = {label:{} for label in labels}
    numberOfIndicators = len(c3d_file['data']['points'][0])  # Count of all indicators ('LASI', 'RASI', etc.)
    numberOfFramesPerIndicator = len(c3d_file['data']['points'][0][0]) # Number of frames per indicator
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
    midStance_r, midStance_l = findMidStance(data, frameRate, globalEvents['times'], globalEvents['foot'], globalEvents['labels'])
    print(globalEvents)






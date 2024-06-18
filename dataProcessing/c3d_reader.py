import ezc3d
import pandas as pd
import numpy as np
from phase_extractor import findMidStance, findTerminalStance, findLoadingResponse

# This function extracts the data from the xlsx file and returns a DataFrame containing the LO evaluation.
def readXLSX(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name='Blad1', header=None)

    # Initialize lists for variable names and values
    variable_names = []
    variable_values = []

    # Iterate through the entire column in steps of 3
    for i in range(0, len(df) - 2, 3):
        if pd.notna(df.iloc[i + 1, 0]):  # Check if the name cell is not empty
            name = df.iloc[i + 1, 0]
            value = df.iloc[i + 2, 0]
            variable_names.append(name)
            variable_values.append(value)

    # Create a DataFrame containing the variable names and values
    d = {'Variable': variable_names, 'Value': variable_values}
    df = pd.DataFrame(d)
    df = df.replace(r'\s+', '', regex=True)
    return df

# This function extracts the data from the c3d file and returns a DataFrame containing the events of the gait cycles.
def readC3D(file_path):
    # Read the file using ezc3d
    c3d_file = ezc3d.c3d(file_path)
    # Extract the labels and the data from the c3d file
    labels = c3d_file['parameters']['POINT']['LABELS']['value']
    label_values = c3d_file['data']['points']
    data = {label: {} for label in labels}
    numberOfIndicators = len(c3d_file['data']['points'][0])  # Count of all indicators ('LASI', 'RASI', etc.)
    numberOfFramesPerIndicator = len(c3d_file['data']['points'][0][0])  # Number of frames per indicator
    contexts = c3d_file['parameters']['EVENT']['CONTEXTS']['value']
    contexts_labels = c3d_file['parameters']['EVENT']['LABELS']['value']
    contexts_frames = c3d_file['parameters']['EVENT']['TIMES']['value'][1, :]
    frameRate = c3d_file['header']['points']['frame_rate']
    firstFrame = c3d_file['header']['points']['first_frame']
    lastFrame = c3d_file['header']['analogs']['last_frame']

    for i in range(0, numberOfIndicators):
        for j in range(0, numberOfFramesPerIndicator):
            data[labels[i]][j] = []
            for k in range(0, 3):
                data[labels[i]][j].append(label_values[k][i][j])
    df = pd.DataFrame(data)
    LKneeAngle = df['LKneeAngles']
    LKneeAngle = np.array([list(LKneeAngle[elem]) for elem in LKneeAngle.keys()])
    RKneeAngle = df['RKneeAngles']
    RKneeAngle = np.array([list(RKneeAngle[elem]) for elem in RKneeAngle.keys()])
    LHipAngle = df['LHipAngles']
    LHipAngle = np.array([list(LHipAngle[elem]) for elem in LHipAngle.keys()])
    RHipAngle = df['RHipAngles']
    RHipAngle = np.array([list(RHipAngle[elem]) for elem in RHipAngle.keys()])
    LAnkleAngle = df['LAnkleAngles']
    LAnkleAngle = np.array([list(LAnkleAngle[elem]) for elem in LAnkleAngle.keys()])
    RAnkleAngle = df['RAnkleAngles']
    RAnkleAngle = np.array([list(RAnkleAngle[elem]) for elem in RAnkleAngle.keys()])
    LAngles = [LHipAngle, LKneeAngle, LAnkleAngle]
    RAngles = [RHipAngle, RKneeAngle, RAnkleAngle]
    d = {'foot': contexts, 'labels': contexts_labels, 'times': contexts_frames}
    globalEvents = pd.DataFrame(d).sort_values('times').reset_index(drop=True)
    # Extract the midstance, terminal stance and loading response
    midStance_r, midStance_l = findMidStance(data, frameRate, globalEvents['times'], globalEvents['foot'],
                                             globalEvents['labels'])
    terminalStance_r, terminalStance_l = findTerminalStance(frameRate, globalEvents['times'], globalEvents['foot'],
                                                            globalEvents['labels'])
    loadingResponse_r, loadingResponse_l = findLoadingResponse(frameRate, globalEvents['times'], globalEvents['foot'],
                                                               globalEvents['labels'])
    # Create a DataFrame containing the midstance, terminal stance and loading response
    terminalStance = pd.DataFrame({
        'foot': ['Right'] * len(terminalStance_r) + ['Left'] * len(terminalStance_l),
        'labels': ['Terminal Stance'] * (len(terminalStance_r) + len(terminalStance_l)),
        'times': [time for time in terminalStance_r] + [time  for time in terminalStance_l]
    })
    loadingResponse = pd.DataFrame({
        'foot': ['Right'] * len(loadingResponse_r) + ['Left'] * len(loadingResponse_l),
        'labels': ['Loading Response'] * (len(loadingResponse_r) + len(loadingResponse_l)),
        'times': [time for time in loadingResponse_r] + [time for time in loadingResponse_l]
    })

    midStance = pd.DataFrame({'foot': ['Right', 'Left'], 'labels': ['Mid Stance', 'Mid Stance'],
                 'times': [int(midStance_r)/frameRate, int(midStance_l)/frameRate]})
    # Concatenate the midstance, terminal stance and loading response to the global events and sort them by time
    globalEvents = pd.concat([globalEvents, midStance], ignore_index=True)
    globalEvents = pd.concat([globalEvents, terminalStance], ignore_index=True)
    globalEvents = pd.concat([globalEvents, loadingResponse], ignore_index=True)
    globalEvents = globalEvents.sort_values('times').reset_index(drop=True)

    return globalEvents, LAngles, RAngles, firstFrame, lastFrame, frameRate

# This function trims the global events DataFrame to only contain the events that are necessary for the analysis.
# We select the first 2 gait cycles, one for each leg, and we only keep the events that are necessary for the analysis.
def trimGlobals(globalEvents):
    # Initialize the counters for the events
    midStanceCounter = 0
    footStrikeCounter = 0
    loadingResponseCounter = 0
    footOffCounter = 0
    terminalStanceCounter = 0
    firstIndex = 0
    lastIndex = -1
    # Iterate over the global events and count the number of each event
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
        # If we have at least 2 gait cycles for each event, we stop the iteration
        if (footStrikeCounter >= 2 and midStanceCounter >= 2 and footOffCounter >= 2 and
                loadingResponseCounter >= 2 and terminalStanceCounter >= 2):
            # We save the index of the last event
            lastIndex = i
            break

    # Slice the DataFrame up to the current index
    filtered_globalEvents = globalEvents.iloc[firstIndex: lastIndex + 1]
    return filtered_globalEvents









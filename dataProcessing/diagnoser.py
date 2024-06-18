def diagnose_ankle(data, side):
    print(data)
    df_stance = data[data['Foot'] == side]
    df_swing = data[data['Foot'] != side]
    plantar_flag = 0
    results = []

    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        result = {"Foot": row.Foot, "Event": row.Event, "Diagnosis": ""}
        ankle = row['LAnkle'] if side == 'Left' else row['RAnkle']
        if row.Event == 'Foot Strike':
            if ankle == -1:
                result["Diagnosis"] = "Plantarflexion"
            elif ankle == 0:
                result["Diagnosis"] = "No relevant finding"
                plantar_flag = 1
        elif row.Event == 'Loading Response':
            if plantar_flag == 1 and ankle == 0:
                result["Diagnosis"] = "No/decreased plantarflexion"
            else:
                result["Diagnosis"] = "No relevant finding"
        elif row.Event == 'Mid Stance':
            if ankle == -1:
                result["Diagnosis"] = "Plantarflexion"
            else:
                result["Diagnosis"] = "Increased dorsiflexion"
        elif row.Event == 'Terminal Stance':
            if ankle == 1:
                result["Diagnosis"] = "Increased dorsiflexion"
            elif ankle == -1:
                result["Diagnosis"] = "Decreased dorsiflexion"
            elif ankle == 0:
                result["Diagnosis"] = "Ankle range of motion within normal range"
        results.append(result)

    # Diagnosis for the swing phase
    for index, row in df_swing.iterrows():
        result = {"Foot": row.Foot, "Event": row.Event, "Diagnosis": ""}
        ankle = row['LAnkle'] if side == 'Left' else row['RAnkle']
        if row.Event == 'Mid Stance':
            if ankle == -1:
                result["Diagnosis"] = "Plantarflexion other foot"
            else:
                result["Diagnosis"] = "No relevant finding"
        elif row.Event == 'Terminal Stance':
            if ankle == -1:
                result["Diagnosis"] = "Plantarflexion other foot"
            else:
                result["Diagnosis"] = "No relevant finding"
        results.append(result)
    return results

def diagnose_knee(data, side):
    df_stance = data[data['Foot'] == side]
    df_swing = data[data['Foot'] != side]
    results = []

    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        result = {"Foot": row.Foot, "Event": row.Event, "Diagnosis": ""}
        knee = row['LKnee'] if side == 'Left' else row['RKnee']
        if row.Event == 'Foot Strike':
            if knee == 1:
                result["Diagnosis"] = "Increased knee flexion"
            else:
                result["Diagnosis"] = "No relevant finding"
        elif row.Event == 'Loading Response':
            result["Diagnosis"] = "Under Construction"
        elif row.Event == 'Mid Stance':
            result["Diagnosis"] = "Under Construction"
        elif row.Event == 'Terminal Stance':
            if knee == 1:
                result["Diagnosis"] = "Increased knee flexion"
            elif knee == -1:
                result["Diagnosis"] = "Knee hyperextension"
            else:
                result["Diagnosis"] = "No relevant finding"
        results.append(result)

    for index, row in df_swing.iterrows():
        result = {"Foot": row.Foot, "Event": row.Event, "Diagnosis": ""}
        knee = row['LKnee'] if side == 'Left' else row['RKnee']
        if row.Event == 'Foot Strike':
            if knee == -1:
                result["Diagnosis"] = "Decreased knee flexion other foot"
            else:
                result["Diagnosis"] = "No relevant finding"
        results.append(result)
    return results

def diagnose_hip(data, side):
    df_stance = data[data['Foot'] == side]
    df_swing = data[data['Foot'] != side]
    results = []

    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        result = {"Foot": row.Foot, "Event": row.Event, "Diagnosis": ""}
        hip = row['LHip'] if side == 'Left' else row['RHip']
        if row.Event == 'Foot Strike':
            if hip == 1:
                result["Diagnosis"] = "Increased hip flexion"
            else:
                result["Diagnosis"] = "No relevant finding"
        results.append(result)
    return results

def diagnose(data):
    results = []
    results.extend(diagnose_ankle(data, 'Left'))
    results.extend(diagnose_ankle(data, 'Right'))
    results.extend(diagnose_knee(data, 'Left'))
    results.extend(diagnose_knee(data, 'Right'))
    results.extend(diagnose_hip(data, 'Left'))
    results.extend(diagnose_hip(data, 'Right'))
    return results

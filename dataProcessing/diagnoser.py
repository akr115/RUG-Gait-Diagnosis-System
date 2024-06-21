import numpy as np
import pandas as pd
def lo_list_creator(list_of_values, variable_names, variable_values):
    lo_df = []
    for i in range(len(list_of_values)):
        lo_df.append([list_of_values[i], find_value_in_list(list_of_values[i], variable_names, variable_values)])
    return lo_df
def find_value_in_list(value, variable_names, variable_values):
    for i in range(len(variable_names)):
        if variable_names[i] == value:
            return variable_values[i]
    return None
#TODO: Seperate the LO and the diagnosis, ensure no duplicates
def diagnose_ankle(data, lo_variable_names, lo_variable_values, side):
    df_stance =  data[data['Foot'] == side]
    df_swing = data[data['Foot'] != side]
    plantar_flag = 0
    result_labels = ["Diagnosis", "LO", "Joint Foot", "Joint", "Event Foot", "Event"]
    joint = "Ankle"
    results = []
    lo_df = []

    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        # Access the associated joint angle with the side
        ankle = row['LAnkle'] if side == 'Left' else row['RAnkle']
        ankle_degrees = row['LAnkle Degrees'] if side == 'Left' else row['RAnkle Degrees']
        if row.Event == 'Foot Strike':
            if ankle == -1:
                # Plantarflexion
                if side == 'Left':
                    lo_variables = ["DorsiflexieMRCLinks", "DorsiflexiegebogenPROMLinks", "DorsiflexiegebogenAOCLinks",
                                    "DorsiflexiegestrektPROMLinks", "DorsiflexiegestrektAOCLinks"]
                    lo_df = lo_list_creator(lo_variables, lo_variable_names, lo_variable_values)
                else:
                    lo_variables = ["DorsiflexieMRCRechts", "DorsiflexiegebogenPROMRechts",
                                    "DorsiflexiegebogenAOCRechts", "DorsiflexiegestrektPROMRechts",
                                    "DorsiflexiegestrektAOCRechts"]
                    lo_df = lo_list_creator(lo_variables, lo_variable_names, lo_variable_values)

                results.append([f"Plantairflexie ({str(np.round(ankle_degrees))} graden)", lo_df, side,
                               joint, row.Foot, row.Event])
            else:
                # No relevant finding in this case
                results.append(["Geen relevante bevindingen", lo_df, side, joint, row.Foot, row.Event])
                plantar_flag = 1
        elif row.Event == 'Loading Response':
            if plantar_flag == 1 and ankle == 0:
                # No/decreased plantarflexion
                results.append([f"Geen/afgenomen plantairflexiebeweging", lo_df, side, joint, row.Foot, row.Event])
            else:
                # No relevant finding in this case
                results.append(["Geen relevante bevindingen", lo_df, side,
                               joint, row.Foot, row.Event])
        elif row.Event == 'Mid Stance':
            if ankle == -1:
                # Plantarflexion
                results.append([f"Plantarflexie ({str(np.round(ankle_degrees))} graden)", lo_df,
                                side, joint, row.Foot, row.Event])
            elif ankle == 1:
                # Increased dorsiflexion
                results.append(["Toegenomen dorsaalflexie", lo_df, side,
                               joint, row.Foot, row.Event])
            else:
                # Ankle range of motion within normal range
                results.append([f"Enkel range of motion ({str(np.round(ankle_degrees))} graden) binnen "
                               f"range van normaal", lo_df,
                                side, joint, row.Foot, row.Event])
        elif row.Event == 'Terminal Stance':
            if ankle == -1:
                # Decreased dorsiflexion
                if side == 'Left':
                    lo_varible = ["DorsiflexiegebogenPROMLinks", "DorsiflexiegebogenAOCLinks",
                                  "DorsiflexiegestrektPROMLinks", "DorsiflexiegestrektAOCLinks"]
                    lo_df = lo_list_creator(lo_varible, lo_variable_names, lo_variable_values)
                else:
                    lo_varible = ["DorsiflexiegebogenPROMRechts", "DorsiflexiegebogenAOCRechts",
                                    "DorsiflexiegestrektPROMRechts", "DorsiflexiegestrektAOCRechts"]
                    lo_df = lo_list_creator(lo_varible, lo_variable_names, lo_variable_values)

                results.append([f"Afgenomen dorsaalflexie ({str(np.round(ankle_degrees))} graden)", lo_df,
                                side, joint, row.Foot, row.Event])
            elif ankle == 1:
                # Increased dorsiflexion
                results.append([f"Toegenomen dorsaalflexie ({str(np.round(ankle_degrees))} graden)", lo_df,
                                side, joint, row.Foot, row.Event])
            else:
                # Ankle range of motion within normal range
                results.append([f"Enkel range of motion ({str(np.round(ankle_degrees))} graden) binnen "
                                 f"range van normaal", lo_df,
                                side, joint, row.Foot, row.Event])
        lo_df = []

    # Diagnosis for the swing phase
    for index, row in df_swing.iterrows():
        # Access the associated joint angle with the side
        ankle = row['LAnkle'] if side != 'Left' else row['RAnkle']
        ankle_degrees = row['LAnkle Degrees'] if side != 'Left' else row['RAnkle Degrees']
        if row.Event == 'Mid Stance':
            if ankle == -1:
                # Plantarflexion other foot
                if side == 'Left':
                    lo_varible = ["DorsiflexieMRCLinks", "DorsiflexiegebogenPROMLinks", "DorsiflexiegebogenAOCLinks",
                                  "DorsiflexiegestrektPROMLinks", "DorsiflexiegestrektAOCLinks"]
                    lo_df = lo_list_creator(lo_varible, lo_variable_names, lo_variable_values)
                else:
                    lo_varible = ["DorsiflexieMRCRechts", "DorsiflexiegebogenPROMRechts", "DorsiflexiegebogenAOCRechts",
                                    "DorsiflexiegestrektPROMRechts", "DorsiflexiegestrektAOCRechts"]
                    lo_df = lo_list_creator(lo_varible, lo_variable_names, lo_variable_values)
                results.append([f"Plantarflexie andere voet ({str(np.round(ankle_degrees))} graden)", lo_df,
                                side, joint, row.Foot, row.Event])
            else:
                results.append(["Geen relevante bevindingen", lo_df, side,
                               joint, row.Foot, row.Event])
        elif row.Event == 'Terminal Stance':
            if ankle == -1:
                # Plantarflexion other foot
                if side == 'Left':
                    lo_varible = ["DorsiflexieMRCLinks", "DorsiflexiegebogenPROMLinks", "DorsiflexiegebogenAOCLinks",
                                    "DorsiflexiegestrektPROMLinks", "DorsiflexiegestrektAOCLinks"]
                    lo_df = lo_list_creator(lo_varible, lo_variable_names, lo_variable_values)
                else:
                    lo_varible = ["DorsiflexieMRCRechts", "DorsiflexiegebogenPROMRechts", "DorsiflexiegebogenAOCRechts",
                                    "DorsiflexiegestrektPROMRechts", "DorsiflexiegestrektAOCRechts"]
                    lo_df = lo_list_creator(lo_varible, lo_variable_names, lo_variable_values)
                results.append([f"Plantarflexie andere voet ({str(np.round(ankle_degrees))} graden)", lo_df,
                                side, joint, row.Foot, row.Event])
            else:
                results.append(["Geen relevante bevindingen", lo_df, side,
                               joint, row.Foot, row.Event])
        lo_df = []
    return pd.DataFrame(results, columns=result_labels)

def diagnose_knee(data, lo_variable_names, lo_variable_values, side):
    df_stance =  data[data['Foot'] == side]
    df_swing = data[data['Foot'] != side]
    result_labels = ["Diagnosis", "LO", "Joint Foot", "Joint", "Event Foot", "Event"]
    joint = "Knee"
    results = []
    lo_df = []
    knee_midstance_threshold = -4

    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        knee = row['LKnee'] if side == 'Left' else row['RKnee']
        knee_degrees = row['LKnee Degrees'] if side == 'Left' else row['RKnee Degrees']
        if row.Event == 'Foot Strike':
            if knee == 1:
                if side == 'Left':
                    lo_variable = ["Pop-hoekPROMLinks", "Pop-hoekAOCLinks", "Knie-extensiePROMLinks"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                else:
                    lo_variable = ["Pop-hoekPROMRechts", "Pop-hoekAOCRechts", "Knie-extensiePROMRechts"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)

                # Increased knee flexion
                results.append([f"Toegenomen knieflexie ({str(np.round(knee_degrees))} graden)", lo_df, side,
                               joint, row.Foot, row.Event])
            else:
                results.append(["Geen relevante bevindingen", lo_df, side,
                               joint, row.Foot, row.Event])
        elif row.Event == 'Loading Response':
            if knee == 1:
                results.append([f"Toegenomen knieflexie ({str(np.round(knee_degrees))} graden) tijdens", lo_df, side,
                               joint, row.Foot, row.Event])
            elif knee == 1:
                if knee_degrees >= 0:
                    # TODO: Knee Moment
                    results.append([f"Afgenomen knieflexie ({str(np.round(knee_degrees))} graden) tijdens", lo_df, side,
                               joint, row.Foot, row.Event])
                else:
                    results.append([f"Knie-extensiemomenten tijdens", lo_df, side,
                               joint, row.Foot, row.Event])
            else:
                results.append(["Geen relevante bevindingen tijdens", lo_df, side,
                               joint, row.Foot, row.Event])
        elif row.Event == 'Mid Stance':
            if knee == 1:
                # Increased knee flexion
                if side == 'Left':
                    lo_variable = ["Knie-extensiePROMLinks", "HeupextensiePROMLinks"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                else:
                    lo_variable = ["Knie-extensiePROMRechts", "HeupextensiePROMRechts"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                results.append([f"Toegenomen knieflexie ({str(np.round(knee_degrees))} graden)", lo_df, side,
                               joint, row.Foot, row.Event])
            elif knee == -1:
                if side == 'Left':
                    lo_variable = ["DorsiflexiegebogenPROMLinks", "DorsiflexiegebogenAOCLinks",
                                    "DorsiflexiegestrektPROMLinks", "DorsiflexiegestrektAOCLinks"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                else:
                    lo_variable = ["DorsiflexiegebogenPROMRechts", "DorsiflexiegebogenAOCRechts",
                                    "DorsiflexiegestrektPROMRechts", "DorsiflexiegestrektAOCRechts"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                if knee_degrees > knee_midstance_threshold:
                    # Decreased knee flexion
                        #TODO: Knee Saggital Moment
                        results.append([f"Afgenomen knieflexie ({str(np.round(knee_degrees))} graden)", lo_df, side,
                               joint, row.Foot, row.Event])
                else:
                    # Knee Hyperextension
                    # TODO: Knee moment Saggital
                    results.append([f"Kniehyperextensie ({str(np.round(knee_degrees))} graden)", lo_df, side,
                               joint, row.Foot, row.Event])
            else:
                results.append(["Geen relevante bevindingen", lo_df, side,
                               joint, row.Foot, row.Event])
        elif row.Event == 'Terminal Stance':
            if knee == 1:
                # Increased knee flexion
                #TODO: Knee Saggital Moment
                if side == 'Left':
                    lo_variable = ["Knie-extensiePROMLinks", "HeupextensiePROMLinks"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                else:
                    lo_variable = ["Knie-extensiePROMRechts", "HeupextensiePROMRechts"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                results.append([f"Toegenomen knieflexie ({str(np.round(knee_degrees))} graden)", lo_df, side,
                               joint, row.Foot, row.Event])
            elif knee == -1:
                #  Knee hyperextension
                if side == 'Left':
                    lo_variable = ["DorsiflexiegebogenPROMLinks", "DorsiflexiegebogenAOCLinks",
                                    "DorsiflexiegestrektPROMLinks", "DorsiflexiegestrektAOCLinks"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                else:
                    lo_variable = ["DorsiflexiegebogenPROMRechts", "DorsiflexiegebogenAOCRechts",
                                    "DorsiflexiegestrektPROMRechts", "DorsiflexiegestrektAOCRechts"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                results.append([f"Kniehyperextensie ({str(np.round(knee_degrees))} graden)", lo_df, side,
                               joint, row.Foot, row.Event])
            else:
                results.append(["Geen relevante bevindingen", lo_df,  side,
                               joint, row.Foot, row.Event])
        lo_df = []

    for index, row  in df_swing.iterrows():
        knee = row['LKnee'] if side == 'Left' else row['RKnee']
        knee_degrees = row['LKnee Degrees'] if side == 'Left' else row['RKnee Degrees']
        if row.Event == 'Foot Strike':
            if knee == -1:
                # Decreased knee flexion other foot
                if side == "Left":
                    lo_variable = ["Duncan-ElyPROMLinks", "Duncan-ElyAOCLinks"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                else:
                    lo_variable = ["Duncan-ElyPROMRechts", "Duncan-ElyAOCRechts"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                results.append([f"Afgenomen knieflexie ({str(np.round(knee_degrees))} graden) bij "
                                 f"andere voet", lo_df, side, joint, row.Foot, row.Event])
            else:
                results.append(["Geen relevante bevindingen", lo_df, side, joint, row.Foot, row.Event])
        lo_df = []

    return pd.DataFrame(results, columns=result_labels)
def diagnose_hip(data, lo_variable_names, lo_variable_values, side):
    df_stance =  data[data['Foot'] == side]
    result_labels = ["Diagnosis", "LO", "Joint Foot", "Joint", "Event Foot", "Event"]
    joint = "Hip"
    results = []
    lo_df = []
    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        if row.Event == 'Foot Strike' or row.Event == 'Loading Response' or row.Event == 'Mid Stance':
            # Access the associated joint angle with the side
            hip = row['LHip'] if side == 'Left' else row['RHip']
            if hip == 1:
                if row.Event == 'Mid Stance':
                    if side == 'Left':
                        lo_variable = ["Knie-extensiePROMLinks", "HeupextensiePROMLinks"]
                        lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                    else:
                        lo_variable = ["Knie-extensiePROMRechts", "HeupextensiePROMRechts"]
                        lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                results.append([f"Toegenomen heupflexie", lo_df, side, joint, row.Foot, row.Event])
            elif hip == -1:
                results.append([f"Afgenomen heupflexie", lo_df, side, joint, row.Foot, row.Event])
            else:
                results.append([f"Geen relevante bevindingen tijdens", lo_df, side, joint, row.Foot, row.Event])
        if row.Event == 'Terminal Stance':
            hip = row['LHip'] if side == 'Left' else row['RHip']
            if hip == 1:
                if side == 'Left':
                    lo_variable = ["Knie-extensiePROMLinks", "HeupextensiePROMLinks", "HeupextensieMRCLinks"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                else:
                    lo_variable = ["Knie-extensiePROMRechts", "HeupextensiePROMRechts", "HeupextensieMRCRechts"]
                    lo_df = lo_list_creator(lo_variable, lo_variable_names, lo_variable_values)
                results.append([f"Geen Heupextensie", lo_df,  side, joint, row.Foot, row.Event])
            else:
                results.append([f"Geen relevante bevindingen tijdens", lo_df, side, joint, row.Foot, row.Event])
        lo_df = []

    return pd.DataFrame(results, columns=result_labels)

def diagnose(data, varible_names, variable_values):
    left_side = []
    right_side = []
    left_side.append(diagnose_ankle(data, varible_names, variable_values, 'Left'))
    left_side.append(diagnose_knee(data, varible_names, variable_values, 'Left'))
    left_side.append(diagnose_hip(data, varible_names, variable_values, 'Left'))
    left_side = pd.concat(left_side, ignore_index=True)
    right_side.append(diagnose_ankle(data, varible_names, variable_values, 'Right'))
    right_side.append(diagnose_knee(data, varible_names, variable_values, 'Right'))
    right_side.append(diagnose_hip(data, varible_names, variable_values, 'Right'))
    right_side = pd.concat(right_side, ignore_index=True)
    result = pd.concat([left_side, right_side], ignore_index=True)
    result = result.sort_values('Event').reset_index(drop=True)
    return result
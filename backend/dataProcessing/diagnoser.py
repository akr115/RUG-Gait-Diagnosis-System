import numpy as np
import pandas as pd

result_labels = ["Diagnosis", "Joint Foot", "Joint", "Event Foot", "Event"]

# This function creates a list containing the variable names and their values that are relevant for this diagnosis.
def lo_list_creator(list_of_values, variable_names, variable_values):
    lo_df = []
    for i in range(len(list_of_values)):
        lo_df.append([list_of_values[i], find_value_in_list(list_of_values[i], variable_names, variable_values)])
    return lo_df
# This function finds the value of a variable in a list of variable names and values.
def find_value_in_list(value, variable_names, variable_values):
    for i in range(len(variable_names)):
        if variable_names[i] == value:
            return variable_values[i]
    return None

# This function diagnoses the ankle joint based on the data, variable names and values and the side of the foot.
def diagnose_ankle(data, side):
    df_stance =  data[data['Foot'] == side]
    df_swing = data[data['Foot'] != side]
    plantar_flag = 0
    lo_variables = []
    joint = "Ankle"
    results = []

    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        # Access the associated joint angle with the side
        ankle = row['LAnkle'] if side == 'Left' else row['RAnkle']
        ankle_degrees = row['LAnkle Degrees'] if side == 'Left' else row['RAnkle Degrees']
        if row.Event == 'Foot Strike':
            if ankle == -1:
                # Plantarflexion
                if side == 'Left':
                    # Extract relevant variables for the LO
                    lo_variables.extend(["DorsiflexieMRCLinks", "DorsiflexiegebogenPROMLinks", "DorsiflexiegebogenAOCLinks",
                                    "DorsiflexiegestrektPROMLinks", "DorsiflexiegestrektAOCLinks"])
                else:
                    # Extract relevant variables for the LO
                    lo_variables.extend(["DorsiflexieMRCRechts", "DorsiflexiegebogenPROMRechts",
                                    "DorsiflexiegebogenAOCRechts", "DorsiflexiegestrektPROMRechts",
                                    "DorsiflexiegestrektAOCRechts"])
                results.append([f"Plantairflexie ({str(np.round(ankle_degrees))} graden)",  side,
                               joint, row.Foot, row.Event])
            else:
                # No relevant finding in this case
                results.append(["Geen relevante bevindingen", side, joint, row.Foot, row.Event])
                plantar_flag = 1
        elif row.Event == 'Loading Response':
            if plantar_flag == 1 and ankle == -1:
                # No/decreased plantarflexion
                results.append([f"Geen/afgenomen plantairflexiebeweging", side, joint, row.Foot, row.Event])
            else:
                # No relevant finding in this case
                results.append(["Geen relevante bevindingen", side,
                               joint, row.Foot, row.Event])
        elif row.Event == 'Mid Stance':
            if ankle == -1:
                # Plantarflexion
                results.append([f"Plantarflexie ({str(np.round(ankle_degrees))} graden)",
                                side, joint, row.Foot, row.Event])
            elif ankle == 1:
                # Increased dorsiflexion
                results.append(["Toegenomen dorsaalflexie",  side,
                               joint, row.Foot, row.Event])
            else:
                # Ankle range of motion within normal range
                results.append([f"Enkel range of motion ({str(np.round(ankle_degrees))} graden) binnen "
                               f"range van normaal",
                                side, joint, row.Foot, row.Event])
        elif row.Event == 'Terminal Stance':
            if ankle == -1:
                # Decreased dorsiflexion
                if side == 'Left':
                    # Extract relevant variables for the LO
                    lo_variables.extend(["DorsiflexiegebogenPROMLinks", "DorsiflexiegebogenAOCLinks",
                                  "DorsiflexiegestrektPROMLinks", "DorsiflexiegestrektAOCLinks"])
                else:
                    # Extract relevant variables for the LO
                    lo_variables.extend(["DorsiflexiegebogenPROMRechts", "DorsiflexiegebogenAOCRechts",
                                    "DorsiflexiegestrektPROMRechts", "DorsiflexiegestrektAOCRechts"])
                results.append([f"Afgenomen dorsaalflexie ({str(np.round(ankle_degrees))} graden)",
                                side, joint, row.Foot, row.Event])
            elif ankle == 1:
                # Increased dorsiflexion
                results.append([f"Toegenomen dorsaalflexie ({str(np.round(ankle_degrees))} graden)",
                                side, joint, row.Foot, row.Event])
            else:
                # Ankle range of motion within normal range
                results.append([f"Enkel range of motion ({str(np.round(ankle_degrees))} graden) binnen "
                                 f"range van normaal",
                                side, joint, row.Foot, row.Event])
    # Diagnosis for the swing phase
    for index, row in df_swing.iterrows():
        # Access the associated joint angle with the side
        ankle = row['LAnkle'] if side != 'Left' else row['RAnkle']
        ankle_degrees = row['LAnkle Degrees'] if side != 'Left' else row['RAnkle Degrees']
        if row.Event == 'Mid Stance':
            if ankle == -1:
                # Plantarflexion other foot
                if side == 'Left':
                    # Extract relevant variables for the LO
                    lo_variables.extend(["DorsiflexieMRCLinks", "DorsiflexiegebogenPROMLinks",
                                         "DorsiflexiegebogenAOCLinks", "DorsiflexiegestrektPROMLinks",
                                         "DorsiflexiegestrektAOCLinks"])
                else:
                    # Extract relevant variables for the LO
                    lo_variables.extend(["DorsiflexieMRCRechts", "DorsiflexiegebogenPROMRechts",
                                         "DorsiflexiegebogenAOCRechts", "DorsiflexiegestrektPROMRechts",
                                         "DorsiflexiegestrektAOCRechts"])
                results.append([f"Plantarflexie andere voet ({str(np.round(ankle_degrees))} graden)",
                                side, joint, row.Foot, row.Event])
            else:
                # No relevant finding in this case
                results.append(["Geen relevante bevindingen",  side,
                               joint, row.Foot, row.Event])
        elif row.Event == 'Terminal Stance':
            if ankle == -1:
                # Plantarflexion other foot
                if side == 'Left':
                    lo_variables.extend(["DorsiflexieMRCLinks", "DorsiflexiegebogenPROMLinks", "DorsiflexiegebogenAOCLinks",
                                    "DorsiflexiegestrektPROMLinks", "DorsiflexiegestrektAOCLinks"])
                else:
                    lo_variables.extend( ["DorsiflexieMRCRechts", "DorsiflexiegebogenPROMRechts", "DorsiflexiegebogenAOCRechts",
                                    "DorsiflexiegestrektPROMRechts", "DorsiflexiegestrektAOCRechts"])
                results.append([f"Plantarflexie andere voet ({str(np.round(ankle_degrees))} graden)",
                                side, joint, row.Foot, row.Event])
            else:
                # No relevant finding in this case
                results.append(["Geen relevante bevindingen",  side,
                               joint, row.Foot, row.Event])
    # Return the results and the list of relevant variables
    return pd.DataFrame(results, columns=result_labels), lo_variables

# This function diagnoses the knee joint based on the data, variable names and values and the side of the foot.
def diagnose_knee(data, side):
    df_stance =  data[data['Foot'] == side]
    df_swing = data[data['Foot'] != side]
    joint = "Knee"
    results = []
    lo_variables = []
    knee_midstance_threshold = -4

    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        knee = row['LKnee'] if side == 'Left' else row['RKnee']
        knee_degrees = row['LKnee Degrees'] if side == 'Left' else row['RKnee Degrees']
        if row.Event == 'Foot Strike':
            if knee == 1:
                if side == 'Left':
                    # Extract relevant variables for the LO
                    lo_variables.extend(["Pop-hoekPROMLinks", "Pop-hoekAOCLinks", "Knie-extensiePROMLinks"])
                else:
                    # Extract relevant variables for the LO
                    lo_variables.extend(["Pop-hoekPROMRechts", "Pop-hoekAOCRechts", "Knie-extensiePROMRechts"])
                # Increased knee flexion
                results.append([f"Toegenomen knieflexie ({str(np.round(knee_degrees))} graden)",  side,
                               joint, row.Foot, row.Event])
            else:
                # No relevant finding in this case
                results.append(["Geen relevante bevindingen", side,
                               joint, row.Foot, row.Event])
        elif row.Event == 'Loading Response':
            if knee == 1:
                # Increased knee flexion
                results.append([f"Toegenomen knieflexie ({str(np.round(knee_degrees))} graden) tijdens",  side,
                               joint, row.Foot, row.Event])
            elif knee == -1:
                if knee_degrees >= 0:
                    # TODO: Knee Moment Saggital
                    # Decreased knee flexion
                    results.append([f"Afgenomen knieflexie ({str(np.round(knee_degrees))} graden) tijdens",  side,
                               joint, row.Foot, row.Event])
                else:
                    # Knee Hyperextension
                    results.append([f"Knie-extensiemomenten tijdens",  side,
                               joint, row.Foot, row.Event])
            else:
                results.append(["Geen relevante bevindingen tijdens",  side,
                               joint, row.Foot, row.Event])
        elif row.Event == 'Mid Stance':
            if knee == 1:
                # Increased knee flexion
                if side == 'Left':
                    # Extract relevant variables for the LO
                    lo_variables.extend(["Knie-extensiePROMLinks", "HeupextensiePROMLinks"])
                else:
                    # Extract relevant variables for the LO
                    lo_variables.extend(["Knie-extensiePROMRechts", "HeupextensiePROMRechts"])
                results.append([f"Toegenomen knieflexie ({str(np.round(knee_degrees))} graden)",  side,
                               joint, row.Foot, row.Event])
            elif knee == -1:
                if side == 'Left':
                    # Extract relevant variables for the LO
                    lo_variables.extend(["DorsiflexiegebogenPROMLinks", "DorsiflexiegebogenAOCLinks",
                                    "DorsiflexiegestrektPROMLinks", "DorsiflexiegestrektAOCLinks"])
                else:
                    # Extract relevant variables for the LO
                    lo_variables.extend(["DorsiflexiegebogenPROMRechts", "DorsiflexiegebogenAOCRechts",
                                    "DorsiflexiegestrektPROMRechts", "DorsiflexiegestrektAOCRechts"])
                if knee_degrees > knee_midstance_threshold:
                    # Decreased knee flexion
                        #TODO: Knee Saggital Moment
                        results.append([f"Afgenomen knieflexie ({str(np.round(knee_degrees))} graden)", side,
                               joint, row.Foot, row.Event])
                else:
                    # Knee Hyperextension
                    # TODO: Knee moment Saggital
                    results.append([f"Kniehyperextensie ({str(np.round(knee_degrees))} graden)",  side,
                               joint, row.Foot, row.Event])
            else:
                # No relevant finding in this case
                results.append(["Geen relevante bevindingen",  side,
                               joint, row.Foot, row.Event])
        elif row.Event == 'Terminal Stance':
            if knee == 1:
                # Increased knee flexion
                #TODO: Knee Saggital Moment
                if side == 'Left':
                    # Extract relevant variables for the LO
                    lo_variables.extend(["Knie-extensiePROMLinks", "HeupextensiePROMLinks"])
                else:
                    # Extract relevant variables for the LO
                    lo_variables.extend(["Knie-extensiePROMRechts", "HeupextensiePROMRechts"])
                results.append([f"Toegenomen knieflexie ({str(np.round(knee_degrees))} graden)",  side,
                               joint, row.Foot, row.Event])
            elif knee == -1:
                #  Knee hyperextension
                if side == 'Left':
                    # Extract relevant variables for the LO
                    lo_variables.extend(["DorsiflexiegebogenPROMLinks", "DorsiflexiegebogenAOCLinks",
                                    "DorsiflexiegestrektPROMLinks", "DorsiflexiegestrektAOCLinks"])
                else:
                    # Extract relevant variables for the LO
                    lo_variables.extend(["DorsiflexiegebogenPROMRechts", "DorsiflexiegebogenAOCRechts",
                                    "DorsiflexiegestrektPROMRechts", "DorsiflexiegestrektAOCRechts"])
                results.append([f"Kniehyperextensie ({str(np.round(knee_degrees))} graden)",  side,
                               joint, row.Foot, row.Event])
            else:
                # No relevant finding in this case
                results.append(["Geen relevante bevindingen", side,
                               joint, row.Foot, row.Event])
    # Diagnosis for the swing phase
    for index, row  in df_swing.iterrows():
        knee = row['LKnee'] if side == 'Left' else row['RKnee']
        knee_degrees = row['LKnee Degrees'] if side == 'Left' else row['RKnee Degrees']
        if row.Event == 'Foot Strike':
            if knee == -1:
                # Decreased knee flexion other foot
                if side == "Left":
                    # Extract relevant variables for the LO
                    lo_variables.extend(["Duncan-ElyPROMLinks", "Duncan-ElyAOCLinks"])
                else:
                    # Extract relevant variables for the LO
                    lo_variables.extend(["Duncan-ElyPROMRechts", "Duncan-ElyAOCRechts"])
                results.append([f"Afgenomen knieflexie ({str(np.round(knee_degrees))} graden) bij "
                                 f"andere voet", side, joint, row.Foot, row.Event])
            else:
                # No relevant finding in this case
                results.append(["Geen relevante bevindingen",  side, joint, row.Foot, row.Event])
    # Return the results and the list of relevant variables
    return pd.DataFrame(results, columns=result_labels), lo_variables
# This function diagnoses the hip joint based on the data, variable names and values and the side of the foot.
def diagnose_hip(data, side):
    df_stance =  data[data['Foot'] == side]
    joint = "Hip"
    results = []
    lo_variables = []

    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        if row.Event == 'Foot Strike' or row.Event == 'Loading Response' or row.Event == 'Mid Stance':
            # Access the associated joint angle with the side
            hip = row['LHip'] if side == 'Left' else row['RHip']
            if hip == 1:
                if row.Event == 'Mid Stance':
                    # Increased hip flexion
                    if side == 'Left':
                        # Extract relevant variables for the LO
                        lo_variables.extend(["Knie-extensiePROMLinks", "HeupextensiePROMLinks"])
                    else:
                        # Extract relevant variables for the LO
                        lo_variables.extend(["Knie-extensiePROMRechts", "HeupextensiePROMRechts"])
                results.append([f"Toegenomen heupflexie", side, joint, row.Foot, row.Event])
            elif hip == -1:
                # Decreased hip flexion
                results.append([f"Afgenomen heupflexie",  side, joint, row.Foot, row.Event])
            else:
                # No relevant finding in this case
                results.append([f"Geen relevante bevindingen tijdens", side, joint, row.Foot, row.Event])
        if row.Event == 'Terminal Stance':
            hip = row['LHip'] if side == 'Left' else row['RHip']
            if hip == 1:
                # No hip extension
                if side == 'Left':
                    # Extract relevant variables for the LO
                    lo_variables.extend( ["Knie-extensiePROMLinks", "HeupextensiePROMLinks", "HeupextensieMRCLinks"])
                else:
                    # Extract relevant variables for the LO
                    lo_variables.extend(["Knie-extensiePROMRechts", "HeupextensiePROMRechts", "HeupextensieMRCRechts"])
                results.append([f"Geen Heupextensie", side, joint, row.Foot, row.Event])
            else:
                # No relevant finding in this case
                results.append([f"Geen relevante bevindingen tijdens",  side, joint, row.Foot, row.Event])
    # Return the results and the list of relevant variables
    return pd.DataFrame(results, columns=result_labels), lo_variables

# This function diagnoses the data based on the data, variable names and values.
def diagnose(data, variable_names, variable_values):
    left_side = []
    right_side = []
    lo = []
    # Diagnose the ankle, knee and hip joints for the left leg
    left,  list_of_lo_names = diagnose_ankle(data, 'Left')
    lo.extend(list_of_lo_names)
    left_side.append(left)
    left, list_of_lo_names = diagnose_knee(data, 'Left')
    lo.extend(list_of_lo_names)
    left_side.append(left)
    left, list_of_lo_names = diagnose_hip(data, 'Left')
    lo.extend(list_of_lo_names)
    left_side.append(left)
    left_side = pd.concat(left_side, ignore_index=True)

    # Diagnose the ankle, knee and hip joints for the right leg
    right, list_of_lo_names = diagnose_ankle(data, 'Right')
    lo.extend(list_of_lo_names)
    right_side.append(right)
    right, list_of_lo_names = diagnose_knee(data, 'Right')
    lo.extend(list_of_lo_names)
    right_side.append(right)
    right, list_of_lo_names = diagnose_hip(data, 'Right')
    lo.extend(list_of_lo_names)
    right_side.append(right)
    right_side = pd.concat(right_side, ignore_index=True)

    # Concatenate the results for the left and right leg
    result = pd.concat([left_side, right_side], ignore_index=True)
    # # Sort the results by the phases of the gait cycle
    columns_sort = ['Event', 'Event Foot']
    result = result.sort_values(columns_sort).reset_index(drop=True)

    # Remove duplicates from the list of relevant variables and
    # Create a DataFrame containing the variable names and values
    lo = list(set(lo))
    lo = lo_list_creator(lo, variable_names, variable_values)
    lo = pd.DataFrame(lo, columns=["Name", "Value"])

    # Return the results and the list of relevant variables
    return result, lo
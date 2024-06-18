import numpy as np
import pandas as pd

#TODO: Add the LO values to the diagnosis
def diagnose_ankle(data, lo_data, side):
    df_stance =  data[data['Foot'] == side]
    df_swing = data[data['Foot'] != side]
    plantar_flag = 0
    result_labels = ["Diagnosis", "LO", "Joint Foot", "Joint", "Event Foot", "Event"]
    joint = "Ankle"
    results = []
    lo_df = pd.DataFrame()

    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        # Access the associated joint angle with the side
        ankle = row['LAnkle'] if side == 'Left' else row['RAnkle']
        ankle_degrees = row['LAnkle Degrees'] if side == 'Left' else row['RAnkle Degrees']
        if row.Event == 'Foot Strike':
            if ankle == -1:
                # Plantarflexion
                if side == 'Left':
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexieMRCLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenPROMLinks"].
                                  reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenAOCLinks"].
                                    reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektPROMLinks"].
                                    reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektAOCLinks"].
                                    reset_index(drop=True)], ignore_index=True)
                else:
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexieMRCRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenPROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenAOCRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektPROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektAOCRechts"].
                                      reset_index(drop=True)], ignore_index=True)

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
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenPROMLinks"].
                                  reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenAOCLinks"].
                                    reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektPROMLinks"].
                                    reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektAOCLinks"].
                                    reset_index(drop=True)], ignore_index=True)
                else:
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenPROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenAOCRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektPROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektAOCRechts"].
                                      reset_index(drop=True)], ignore_index=True)

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
        lo_df = pd.DataFrame()

    # Diagnosis for the swing phase
    for index, row in df_swing.iterrows():
        ankle = row['LAnkle'] if side == 'Left' else row['RAnkle']
        ankle_degrees = row['LAnkle Degrees'] if side == 'Left' else row['RAnkle Degrees']
        if row.Event == 'Mid Stance':
            if ankle == -1:
                # Plantarflexion other foot
                if side == 'Left':
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexieMRCLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenPROMLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenAOCLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektPROMLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektAOCLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                else:
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexieMRCRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenPROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenAOCRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektPROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektAOCRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                results.append([f"Plantarflexie andere voet ({str(np.round(ankle_degrees))} graden)", lo_df,
                                side, joint, row.Foot, row.Event])
            else:
                results.append(["Geen relevante bevindingen", lo_df, side,
                               joint, row.Foot, row.Event])
        elif row.Event == 'Terminal Stance':
            if ankle == -1:
                # Plantarflexion other foot
                if side == 'Left':
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexieMRCLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenPROMLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenAOCLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektPROMLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektAOCLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                else:
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexieMRCRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenPROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenAOCRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektPROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektAOCRechts"].
                                      reset_index(drop=True)], ignore_index=True)

                results.append([f"Plantarflexie andere voet ({str(np.round(ankle_degrees))} graden)", lo_df,
                                side, joint, row.Foot, row.Event])
            else:

                results.append(["Geen relevante bevindingen", lo_df, side,
                               joint, row.Foot, row.Event])
    return pd.DataFrame(results, columns=result_labels)

def diagnose_knee(data, lo_data, side):
    df_stance =  data[data['Foot'] == side]
    df_swing = data[data['Foot'] != side]
    result_labels = ["Diagnosis", "LO", "Joint Foot", "Joint", "Event Foot", "Event"]
    joint = "Knee"
    results = []
    lo_df = pd.DataFrame()

    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        knee = row['LKnee'] if side == 'Left' else row['RKnee']
        knee_degrees = row['LKnee Degrees'] if side == 'Left' else row['RKnee Degrees']
        if row.Event == 'Foot Strike':
            if knee == 1:
                if side == 'Left':
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "Pop-hoekPROMLinks"].
                                      reset_index(drop=True)],ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "Pop-hoekAOCLinks"].
                                        reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "Knie-extensiePROMLinks"].
                                        reset_index(drop=True)], ignore_index=True)
                else:
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "Pop-hoekPROMRechts"].
                                      reset_index(drop=True)],ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "Pop-hoekAOCRechts"].
                                        reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "Knie-extensiePROMRechts"].
                                        reset_index(drop=True)], ignore_index=True)

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
            #TODO: Differentiate between increased and slightly increased knee flexion
            print("Under Construction")
        elif row.Event == 'Terminal Stance':
            if knee == 1:
                # Increased knee flexion
                #TODO: Knee Saggital Moment
                if side == 'Left':
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "Knie-extensiePROMLinks"].
                                      reset_index(drop=True)],ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "HeupextensiePROMLinks"].
                                        reset_index(drop=True)], ignore_index=True)
                else:
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "Knie-extensiePROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "HeupextensiePROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)

                results.append([f"Toegenomen knieflexie ({str(np.round(knee_degrees))} graden)", lo_df, side,
                               joint, row.Foot, row.Event])
            elif knee == -1:
                #  Knee hyperextension
                if side == 'Left':
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenPROMLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenAOCLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektPROMLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektAOCLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                else:
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenPROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegebogenAOCRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektPROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "DorsiflexiegestrektAOCRechts"].
                                      reset_index(drop=True)], ignore_index=True)

                results.append([f"Kniehyperextensie ({str(np.round(knee_degrees))} graden)", lo_df, side,
                               joint, row.Foot, row.Event])
            else:
                results.append(["Geen relevante bevindingen", lo_df,  side,
                               joint, row.Foot, row.Event])
        lo_df = pd.DataFrame()

    for index, row  in df_swing.iterrows():
        knee = row['LKnee'] if side == 'Left' else row['RKnee']
        knee_degrees = row['LKnee Degrees'] if side == 'Left' else row['RKnee Degrees']
        if row.Event == 'Foot Strike':
            if knee == -1:
                # Decreased knee flexion other foot
                if side == "Left":
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "Duncan-ElyPROMLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "Duncan-ElyAOCLinks"].
                                      reset_index(drop=True)], ignore_index=True)
                else:
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "Duncan-ElyPROMRechts"].
                                      reset_index(drop=True)], ignore_index=True)
                    lo_df = pd.concat([lo_df, lo_data[lo_data["Variable"] == "Duncan-ElyAOCRechts"].
                                      reset_index(drop=True)], ignore_index=True)

                results.append([f"Afgenomen knieflexie ({str(np.round(knee_degrees))} graden) bij "
                                 f"andere voet", lo_df, side, joint, row.Foot, row.Event])
            else:
                results.append(["Geen relevante bevindingen", lo_df, side, joint, row.Foot, row.Event])
        lo_df = pd.DataFrame()

    return pd.DataFrame(results, columns=result_labels)
def diagnose_hip(data, lo_data, side):
    #TODO: Determine the difference between increased and decreased hip flexion.
    df_stance =  data[data['Foot'] == side]
    result_labels = ["Diagnosis", "Joint Foot", "Joint", "Event Foot", "Event"]
    joint = "Hip"
    results = []
    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        if row.Event == 'Foot Strike' or row.Event == 'Loading Response' or row.Event == 'Mid Stance':
            # Access the associated joint angle with the side
            hip = row['LHip'] if side == 'Left' else row['RHip']
            if hip == 1:
                # print(f"Toegenomen heupflexie bij {row.Foot} {row.Event}")  # Increased hip flexion
                results.append([f"Toegenomen heupflexie", side, joint, row.Foot, row.Event])
            elif hip == -1:
                # print(f"Afgenomen heupflexie bij {row.Foot} {row.Event}")  # Decreased hip flexion
                results.append([f"Afgenomen heupflexie", side, joint, row.Foot, row.Event])
            else:
                # print(f"Geen relevante bevindingen bij {row.Foot} {row.Event}")
                results.append([f"Geen relevante bevindingen", side, joint, row.Foot, row.Event])

        if row.Event == 'Terminal Stance':
            hip = row['LHip'] if side == 'Left' else row['RHip']
            if hip == 1:
                # print(f"Geen Heupextensie bij {row.Foot} {row.Event}")
                results.append([f"Geen Heupextensie", side, joint, row.Foot, row.Event])
            else:
                # print(f"Geen relevante bevindingen bij {row.Foot} {row.Event}")
                results.append([f"Geen relevante bevindingen", side, joint, row.Foot, row.Event])

    return pd.DataFrame(results, columns=result_labels)

def diagnose(data, lo):
    left_side = []
    right_side = []
    left_side.append(diagnose_ankle(data, lo, 'Left'))
    left_side.append(diagnose_knee(data, lo, 'Left'))
    left_side.append(diagnose_hip(data, lo, 'Left'))
    left_side = pd.concat(left_side, ignore_index=True)
    right_side.append(diagnose_ankle(data, lo, 'Right'))
    right_side.append(diagnose_knee(data, lo,'Right'))
    right_side.append(diagnose_hip(data, lo,'Right'))
    right_side = pd.concat(right_side, ignore_index=True)
    result = pd.concat([left_side, right_side], ignore_index=True)
    result = result.sort_values('Event').reset_index(drop=True)
    return result
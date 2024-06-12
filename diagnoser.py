
def diagnose_ankle(data, side):
    df_stance =  data[data['Foot'] == side]
    df_swing = data[data['Foot'] != side]
    plantar_flag = 0

    # Diagnosis for the stance phase
    for index, row in df_stance.iterrows():
        if row.Event == 'Foot Strike':
            # Access the associated joint angle with the side
            ankle = row['LAnkle'] if side == 'Left' else row['RAnkle']
            if ankle == -1:
                print(f"Plantarflexie bij {row.Foot} {row.Event}")  # Plantarflexion
            elif ankle == 0:
                print(f"Geen relevante bevindingen bij {row.Foot} {row.Event}") # No relevant finding in this case
                plantar_flag = 1
        elif row.Event == 'Loading Response':
            ankle = row['LAnkle'] if side == 'Left' else row['RAnkle']
            if plantar_flag == 1 and ankle == 0:
                # No/decreased plantarflexion
                print(f"Geen/afgenomen plantairflexiebeweging tijdens {row.Foot} {row.Event}")
            else:
                print(f"Geen relevante bevindingen bij {row.Foot} {row.Event}") # No relevant finding in this case
        elif row.Event == 'Mid Stance':
            ankle = row['LAnkle'] if side == 'Left' else row['RAnkle']
            if ankle == -1:
                # TODO: Add the degree of plantarflexion
                print(f"Plantarflexie bij {row.Foot} {row.Event}") # Plantarflexion
            else:
                print(f"Toegenomen dorsaalflexie in {row.Foot} {row.Event}") # Increased dorsiflexion
        elif row.Event == 'Terminal Stance':
            ankle = row['LAnkle'] if side == 'Left' else row['RAnkle']
            if ankle == 1:
                print(f"Toegenomen dorsaalflexie in {row.Foot} {row.Event}") # Increased dorsiflexion
            elif ankle == -1:
                # TODO: Add the degree of flexion
                print(f"`afgenomen dorsaalflexie in {row.Foot} {row.Event}") # Decreased dorsiflexion
            elif ankle == 0:
                # Ankle range of motion within normal range
                # TODO: Add the degree
                print(f"Enkel range of motion binnen range van normal in {row.Foot} {row.Event}")

    #Diagnosis for the swing phase
    for index, row in df_swing.iterrows():
        if row.Event == 'Mid Stance':
            ankle = row['LAnkle'] if side == 'Left' else row['RAnkle']
            if ankle == -1:
                # TODO: Add the degree of plantarflexion
                print(f"Plantarflexie andere voet bij {row.Foot} {row.Event}") # Plantarflexion other foot
            else:
                print(f"Geen relevante bevindingen bij {row.Foot} {row.Event}")
        elif row.Event == 'Terminal Stance':
            ankle = row['LAnkle'] if side == 'Left' else row['RAnkle']
            if ankle == -1:
                # TODO: Add the degree of plantarflexion
                print(f"Plantarflexie andere voet bij {row.Foot} {row.Event}")  # Plantarflexion other foot
            else:
                print(f"Geen relevante bevindingen bij {row.Foot} {row.Event}")



def diagnose(data):
    diagnose_ankle(data, 'Left')
    diagnose_ankle(data, 'Right')
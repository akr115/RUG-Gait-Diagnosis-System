import pyc3dtools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl

# Path to the C3D file
file_path = '/Users/amoor/Downloads/WalkNormal01.c3d'
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2M2VlNDFlY2RmODE2MDk0MTI0ZTEyNjIiLCJpYXQiOjE2ODc0MDk1ODEsImV4cCI6MTY4NzQxMzE4MX0.KwuGt4MNbuR2QcwMy4clRB8waVy0anBcdmDDyCF3y3c"


def detect_midstances(start_frame, end_frame, data):
    x = 0
    y = 1
    z = 2
    left_foot_first = False
    right_foot_first = False
    mid_stance_frames = []
    LKNE = data["LKNE"]
    RKNE = data["RKNE"]
    LANK = data["LANK"]
    RANK = data["RANK"]
    LTOE = data["LTOE"]
    RTOE = data["RTOE"]

    # # Detect whether we have contact with the right foot first or the left foot first
    # if LTOE[start_frame - 1][z] > RTOE[start_frame - 1][z]:
    #     left_foot_first = True
    # else:
    #     right_foot_first = True
    # print(f"Left foot first: {left_foot_first}")
    # print(f"Right foot first: {right_foot_first}")

    # Detect mid stance frames
    # for i in range(start_frame, end_frame):




    return []


def read_c3dtools(file_path):
    try:
        c3d = pyc3dtools.readC3D(TOKEN, file_path)
        if c3d['Status'] == 'Failed':
            print(c3d['error'])
            return None
        else:
            print('C3D file read successfully.')
            return c3d
    except Exception as e:
        print(e)
        return None


def check_start_frame(main_grf_data, start_frame):
    for i in range(len(main_grf_data)):
        if main_grf_data[i][0] > 0 or main_grf_data[i][1] > 0:
            start_frame = i
            break
    return start_frame // 2


def check_end_frame(main_grf_data, end_frame, start_frame):
    for i in range((start_frame * 2), len(main_grf_data)):
        if main_grf_data[i][0] == 0 and main_grf_data[i + 1][0] == 0:
            end_frame = i
            break
    return end_frame // 2


if __name__ == "__main__":
    c3d = read_c3dtools(file_path)
    coordinate = 0
    print(c3d['Header'])
    Number_of_Markers = c3d['Header']['Number_of_Points']
    First_Frame = c3d['Header']['first_frame']
    Last_Frame = c3d['Header']['last_frame']
    Video_Sampling_Rate = c3d['Header']['Video_Frame_Rate']
    Number_of_Analog_Channels = c3d['Header']['Analog_number_channel']
    Analog_Sample_Rate = c3d['Header']['Analog_Frame_Rate']
    Analog_sample_per_video_frame = c3d['Header']['Analog_sample_per_Frame']
    NumFrames = Last_Frame - First_Frame + 1
    Units = c3d['Units']
    Y_SCREEN = c3d['Coordinate system'][1]
    point_lbl = c3d['Markers Label']
    points = c3d['Markers']
    All_Points = c3d['Points']
    Analog_lbl = c3d['Analog Label']
    Analog_data = c3d['Analog']
    GP = c3d['GP']
    print(GP)


    print('---------------------------- C3Dtools.Com ----------------------------')
    print(f"Header::Number of Markers = {Number_of_Markers}")
    print(f"Header::First Frame = {First_Frame}")
    print(f"Header::Last Frame = {Last_Frame}")
    print(f"Header::Video Sampling Rate = {Video_Sampling_Rate}")
    print(f"Header::Analog Channels = {Number_of_Analog_Channels}")
    print(f"Header:: Analog Sample Rate = {Analog_Sample_Rate}")
    print(f"Header:: Analog sample per video frame = {Analog_sample_per_video_frame}")
    print(f"Header:: Number of Frames = {NumFrames}")
    print(f"Header:: Units = {Units}")
    print(f"Header:: Y_SCREEN = {Y_SCREEN}")
    print(f"Analog Label = {Analog_lbl}")
    print(f"Analog Data x dimension= {len(Analog_data)}")
    print(f"Analog Data y dimension= {len(Analog_data[0])}")
    print(f"Analog Data z dimension= {len(Analog_data[0][0])}")

    # Remove last 2 values of every All_Points[][]
    for i in range(len(All_Points)):
        for j in range(len(All_Points[i])):
            All_Points[i][j] = All_Points[i][j][:-2]

    # Forceplate
    Forceplates = c3d['ForcePlate']
    cop_data = []
    grf_vector = []
    corners = []
    for fp in Forceplates:
        # COP
        cop_data.append(fp['COP'])
        # GRF
        grf_vector.append(fp['GRF_VECTOR'])
        # Corners
        for c in range(4):
            corners.extend(fp['corners'])

    # COP & GRF
    main_cop_data = []
    main_grf_data = []

    data = pd.DataFrame(All_Points, columns=point_lbl)
    data.columns = data.columns.str.strip()

    # Detect which frames have a GRF in either forceplate
    start_frame = 0
    end_frame = NumFrames
    for i in range(NumFrames):
        for fp in range(len(Forceplates)):
            main_cop_data.append([cop_data[fp][i, 0, 0], cop_data[fp][i, 1, 0], cop_data[fp][i, 2, 0]])
            main_grf_data.append([grf_vector[fp][i, 0, 0], grf_vector[fp][i, 1, 0], grf_vector[fp][i, 2, 0]])
            # print(f"Frame {i} - Forceplate {fp} - COP: {main_cop_data[-1]} - GRF: {main_grf_data[-1]}")
    print(f"Main GRF Data Size: {len(main_grf_data)}")
    start_frame = check_start_frame(main_grf_data, start_frame)
    end_frame = check_end_frame(main_grf_data, end_frame, start_frame)
    print(f"Start frame: {start_frame}")
    print(f"End frame: {end_frame}")

    # Include the COP and GRF data in the dataframe
    data_cop = []
    data_grf = []

    cop = []
    grf = []
    for fp in range(len(Forceplates)):
        for i in range(NumFrames):
            cop.append([cop_data[fp][i, 0, 0], cop_data[fp][i, 1, 0], cop_data[fp][i, 2, 0]])
            grf.append([grf_vector[fp][i, 0, 0], grf_vector[fp][i, 1, 0], grf_vector[fp][i, 2, 0]])
            # print(f"Frame {i} - Forceplate {fp} - COP: {cop[-1]} - GRF: {grf[-1]}")

        data_cop.append(cop)
        data_grf.append(grf)
        cop = []
        grf = []
    print(f"Data COP Size: {len(data_cop[0])}")
    print(f"Data GRF Size: {len(data_grf[0])}")
    for fp in range(len(Forceplates)):
        data.insert(len(data.columns), f"COP_{fp}", data_cop[fp])
    for fp in range(len(Forceplates)):
        data.insert(len(data.columns), f"GRF_{fp}", data_grf[fp])

    compute_midstance_frames = detect_midstances(start_frame, end_frame, data)




    # XYZ = []
    # d = []
    #
    # for f in All_Points:
    #     XYZ.append('x')
    #     XYZ.append('y')
    #     XYZ.append('z')
    #
    # s1 = pd.Series(XYZ, name="XYZ")
    # data_duplicate = pd.DataFrame(s1)
    # print(data_duplicate.shape)
    #
    # # check the duplicated name in point_lbl
    # for idx, m in enumerate(point_lbl):
    #     counter = 1
    #     for idx2, m2 in enumerate(point_lbl[idx + 1:]):
    #         if m2 == m:
    #             point_lbl[idx + idx2 + 1] = m2 + '-' + str(counter)
    #             counter += 1
    #
    # for m in range(len(point_lbl)):
    #     for f in All_Points:
    #         d.append(f[m][0])
    #         d.append(f[m][1])
    #         d.append(f[m][2])
    #     data.insert(1, point_lbl[m], d)
    #     d = []
    #     # GRF
    # for idx, f in enumerate(Forceplates):
    #     FZ = np.array(f['FZ'])
    #     FZ = FZ[:, 0]
    #     FY = np.array(f['FY'])
    #     FY = FY[:, 0]
    #     FX = np.array(f['FX'])
    #     FX = FX[:, 0]
    #     for k in range(len(FX)):
    #         d.append(FX[k])
    #         d.append(FY[k])
    #         d.append(FZ[k])
    #     data.insert(1, 'GRF' + str(idx), d)
    #     d = []
    #
    #     # Analog
    #     # check the duplicated name in point_lbl
    #     for idx, m in enumerate(Analog_lbl):
    #         counter = 1;
    #         for idx2, m2 in enumerate(Analog_lbl[idx + 1:]):
    #             if m2 == m:
    #                 Analog_lbl[idx + idx2 + 1] = m2 + '-' + str(counter)
    #                 counter += 1
    #
    #     pyg_analog_data = []
    #     for idx, f in enumerate(Analog_lbl):
    #
    #         if len(Analog_data[:, 0, 0]) == 1:
    #             AA_data = Analog_data[:, idx, :].flatten()
    #         else:
    #             AA_data = Analog_data[:, :, idx].flatten()
    #
    #         if len(pyg_analog_data) == 0:
    #             s1 = pd.Series(AA_data, name=f)
    #             pyg_analog_data = pd.DataFrame(s1)
    #         else:
    #             pyg_analog_data.insert(1, f, AA_data)
    # data.columns = data.columns.str.strip()
    # x_data = data[data["XYZ"] == "x"].reset_index(drop=True)
    # y_data = data[data["XYZ"] == "y"].reset_index(drop=True)
    # z_data = data[data["XYZ"] == "z"].reset_index(drop=True)
    #
    # # Compute midstance frames
    # mid_stance_frames = detect_midstances(start_frame, end_frame, x_data, y_data, z_data)
    # print(mid_stance_frames)

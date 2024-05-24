import pyc3dtools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Path to the C3D file
file_path = '/Users/amoor/Downloads/WalkNormal01.c3d'
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2M2VlNDFlY2RmODE2MDk0MTI0ZTEyNjIiLCJpYXQiOjE2ODc0MDk1ODEsImV4cCI6MTY4NzQxMzE4MX0.KwuGt4MNbuR2QcwMy4clRB8waVy0anBcdmDDyCF3y3c"


def detect_walk_phases(c3d):
    points = np.array(c3d['Markers'])
    num_frames = points.shape[0]
    marker_labels = c3d['Markers Label']

    # Assuming 'heel' and 'toe' markers are labeled appropriately
    heel_marker_idx = marker_labels.index('heel') if 'heel' in marker_labels else None
    toe_marker_idx = marker_labels.index('toe') if 'toe' in marker_labels else None

    if heel_marker_idx is None or toe_marker_idx is None:
        raise ValueError("Heel or Toe marker not found in the data.")

    heel_z = points[:, heel_marker_idx, 2]
    toe_z = points[:, toe_marker_idx, 2]

    grf = None
    if 'ForcePlate' in c3d and len(c3d['ForcePlate']) > 0:
        grf = np.array(c3d['ForcePlate'][0]['FZ'][:, 0])

    # Detect Initial Contact (IC)
    ic_frames = np.where((heel_z[1:] < heel_z[:-1]) & (heel_z[:-1] >= heel_z[1:]))[0] + 1

    # Detect Toe Off (TO)
    to_frames = np.where((toe_z[1:] < toe_z[:-1]) & (toe_z[:-1] >= toe_z[1:]))[0] + 1

    # Detect Heel Lift (HL) and Flat Foot (FF) based on heel_z
    hl_frames = np.where((heel_z[1:] > heel_z[:-1]) & (heel_z[:-1] <= heel_z[1:]))[0] + 1
    ff_frames = np.where((heel_z == heel_z.min()))[0]

    # Mid Stance (MS)
    if grf is not None:
        ms_frames = np.where(grf == grf.max())[0]
    else:
        ms_frames = np.where((heel_z + toe_z) / 2 == (heel_z + toe_z).max())[0]

    # Create a dictionary of phases
    phases = {
        'IC': ic_frames,
        'FF': ff_frames,
        'MS': ms_frames,
        'HL': hl_frames,
        'TO': to_frames
    }

    return phases


def split_data_by_phases(data, phases):
    phase_data = {}
    for phase, frames in phases.items():
        phase_data[phase] = data.iloc[frames]
    return phase_data


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


def find_initial_contact(c3d, marker_index):
    points = np.array(c3d['Markers'])
    num_frames = points.shape[0]
    z_positions = points[:, marker_index, 2]  # Vertical positions of the specified marker

    initial_contacts = []
    threshold = np.mean(z_positions) - 0.1 * np.std(z_positions)  # Adjust the threshold as necessary

    for i in range(1, num_frames):
        if z_positions[i] < threshold and z_positions[i - 1] >= threshold:
            initial_contacts.append(i)

    return initial_contacts


def plot_initial_contact(c3d, initial_contacts, marker_index):
    points = np.array(c3d['Markers'])
    x_coords = points[:, marker_index, 0]
    y_coords = points[:, marker_index, 1]
    z_coords = points[:, marker_index, 2]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_coords, y_coords, z_coords, label='Trajectory')

    # Highlight initial contacts
    ax.scatter(x_coords[initial_contacts], y_coords[initial_contacts], z_coords[initial_contacts], c='r',
               label='Initial Contact')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.legend()
    plt.show()


def check_start_frame(main_grf_data, start_frame):
    for i in range(len(main_grf_data)):
        if main_grf_data[i][0] > 0 or main_grf_data[i][1] > 0:
            start_frame = i
            break
    return start_frame // 2


def check_end_frame(main_grf_data, end_frame, start_frame):
    for i in range((start_frame*2), len(main_grf_data)):
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
    NumFrames = Last_Frame - First_Frame
    Units = c3d['Units']
    Y_SCREEN = c3d['Coordinate system'][1]

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

    point_lbl = c3d['Markers Label']
    points = c3d['Markers']
    All_Points = c3d['Points']
    if len(point_lbl) > 0:
        Number_of_actual_Marker = len(points[0, :, 0])
    else:
        Number_of_actual_Marker = 0
    # Analog Data
    Analog_lbl = c3d['Analog Label']
    Analog_data = c3d['Analog']

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

    # 3D Viewer ###################################

    # Markers
    main_point_data = []
    if Number_of_actual_Marker > 0:
        for i in range(NumFrames):
            frame = i
            time = i
            point_data = []
            for j in range(Number_of_actual_Marker):
                if (Y_SCREEN == '-Z' or Y_SCREEN == '+Z'):
                    point_data.append(points[i, j, 0])
                    point_data.append(points[i, j, 2])
                    point_data.append(points[i, j, 1] * -1)

            main_point_data.append(point_data)
    print("---------------Main Point Data------------------")
    print(f"Number of rows: {main_point_data.__len__()}")
    print(f"Number of columns: {main_point_data[0].__len__()}")
    print("-------------------------------------------------")

    # COP & GRF
    main_cop_data = []
    main_grf_data = []

    # Detect which frames have a GRF in either forceplate
    start_frame = 0
    end_frame = NumFrames
    start_frame_flag = False

    for i in range(NumFrames):
        for fp in range(len(Forceplates)):
            main_cop_data.append([cop_data[fp][i, 0, 0], cop_data[fp][i, 1, 0]])
            main_grf_data.append([grf_vector[fp][i, 0, 0], grf_vector[fp][i, 1, 0], grf_vector[fp][i, 2, 0]])
            print(f"Frame {i} - Forceplate {fp} - COP: {main_cop_data[-1]} - GRF: {main_grf_data[-1]}")
    print(len(main_grf_data))
    start_frame = check_start_frame(main_grf_data, start_frame)
    end_frame = check_end_frame(main_grf_data, end_frame, start_frame)
    print(f"Start frame: {start_frame}")
    print(f"End frame: {end_frame}")

    XYZ = []
    d = []

    for f in All_Points:
        XYZ.append('x')
        XYZ.append('y')
        XYZ.append('z')

    s1 = pd.Series(XYZ, name="XYZ")
    data = pd.DataFrame(s1)

    # check the duplicated name in point_lbl
    for idx, m in enumerate(point_lbl):
        counter = 1
        for idx2, m2 in enumerate(point_lbl[idx + 1:]):
            if m2 == m:
                point_lbl[idx + idx2 + 1] = m2 + '-' + str(counter)
                counter += 1

    for m in range(len(point_lbl)):
        for f in All_Points:
            d.append(f[m][0])
            d.append(f[m][1])
            d.append(f[m][2])
        data.insert(1, point_lbl[m], d)
        d = []
        # GRF
    for idx, f in enumerate(Forceplates):
        FZ = np.array(f['FZ'])
        FZ = FZ[:, 0]
        FY = np.array(f['FY'])
        FY = FY[:, 0]
        FX = np.array(f['FX'])
        FX = FX[:, 0]
        for k in range(len(FX)):
            d.append(FX[k])
            d.append(FY[k])
            d.append(FZ[k])
        data.insert(1, 'GRF' + str(idx), d)
        d = []

        # Analog
        # check the duplicated name in point_lbl
        for idx, m in enumerate(Analog_lbl):
            counter = 1;
            for idx2, m2 in enumerate(Analog_lbl[idx + 1:]):
                if m2 == m:
                    Analog_lbl[idx + idx2 + 1] = m2 + '-' + str(counter)
                    counter += 1

        pyg_analog_data = []
        for idx, f in enumerate(Analog_lbl):

            if len(Analog_data[:, 0, 0]) == 1:
                AA_data = Analog_data[:, idx, :].flatten()
            else:
                AA_data = Analog_data[:, :, idx].flatten()

            if len(pyg_analog_data) == 0:
                s1 = pd.Series(AA_data, name=f)
                pyg_analog_data = pd.DataFrame(s1)
            else:
                pyg_analog_data.insert(1, f, AA_data)

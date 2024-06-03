from c3d_reader import readC3D, trimGlobals, readXLSX

if __name__ == "__main__":
    file_path_normal = '/Users/amoor/Downloads/Walk_100_03.c3d'
    file_path = '/Users/amoor/Downloads/WalkNormal01.c3d'
    lo_file_path = '/Users/amoor/Downloads/LO.xlsx'
    lo = readXLSX(lo_file_path)
    global_events_normal = readC3D(file_path_normal)
    global_events = readC3D(file_path)
    global_events = trimGlobals(global_events)
    global_events_normal=trimGlobals(global_events_normal)


    print(global_events_normal)
    print("-----------------------------------")
    print(global_events)

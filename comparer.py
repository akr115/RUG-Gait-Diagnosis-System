import numpy as np

def compareJointAngles(global_events, global_events_normal, LAngles, RAngles, LAnglesNormal, RAnglesNormal):
    midstanceNormLeft = global_events_normal[['foot'] == 'Left' and ['labels'] == 'Mid Stance']
    print(midstanceNormLeft)
    # midstanceNormRight
    # footStrikeNormLeft
    # footStrikeNormRight
    

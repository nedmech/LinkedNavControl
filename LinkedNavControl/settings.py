# SessionComponent size 
numTRACKS = 1
numSCENES = 1

# debug_mode: whether the log-function should output to logfile
debug_mode = False

"""
MIDI Notes and CC numbers to link to control actions
"""

CHAN = 0 # default MIDI Channel for communication (0-15)

STOP_BUTTON              =  0 # C-2
STOP_ALL_CLIPS           =  1 # C#-2
STOP_ALL_CLIPS_NOW       =  2 #D-2

SELECT_FIRST_SCENE       =  4 # E-2
SELECT_PREV_SCENE        =  5 # F-2
SELECT_NEXT_SCENE        =  6 # F#-2
SELECT_LAST_SCENE        =  7 # G-2

PLAY_PREVIOUS_SCENE      =  8 # G#-2
PLAY_SELECTED_SCENE      =  9 # A-2
PLAY_NEXT_SCENE          = 10 # A#-2
SELECT_PLAYING_CLIP_SLOT = 11 # B-2

STOP_SELECTED_TRACK      = 12 # C-1

SELECT_FIRST_TRACK       = 16 # E-1
SELECT_PREV_TRACK        = 17 # F-1
SELECT_NEXT_TRACK        = 18 # F#-1
SELECT_LAST_TRACK        = 19 # G-1

SCENE_BANK_FIRST         = 29 # E0
SCENE_BANK_NEXT          = 29 # F0
SCENE_BANK_PREV          = 30 # F#0
SCENE_BANK_LAST          = 31 # G0


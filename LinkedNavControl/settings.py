# SessionComponent size 
numTRACKS = 8
numSCENES = 1

# debug_mode: whether the log-function should output to log file
debug_mode = False

from MIDI import * # import MIDI status codes

""" settings which MIDI-notes and CCs trigger which functionality """

midi_mapping = {
    "scroll_scene_banks": CC(3),
    "select_scene_bank" : CC(0, ABSOLUTE),

    "scroll_scenes": CC(14),
    "select_scene" : CC(15, ABSOLUTE),

    "scroll_tracks": CC(16),
    "select_track" : CC(17, ABSOLUTE),

    "stop_playing"              : Note( 0), # C-2
    "stop_all_clips"            : Note( 1), # C#-2
    "stop_all_clips_immediately": Note( 2), # D-2
    "stop_click_track"          : Note( 3), # D#-2

    "first_scene"               : Note( 4), # E-2
    "prev_scene"                : Note( 5), # F-2
    "next_scene"                : Note( 6), # F#-2
    "last_scene"                : Note( 7), # G-2

    "play_selected_scene"       : Note( 8), # G#-2
    "play_prev_scene"           : Note( 9), # A-2
    "play_next_scene"           : Note(10), # A#-2
    # highlights clip slot with currently playing clip in selected track
    "select_playing_clip"       : Note(11), # B-2 

    "stop_selected_track"       : Note(12), # C-1
    "mute_selected_track"       : Note(13), # C#-1
    "unmute_selected_track"     : Note(14), # D-1

    "first_track"               : Note(16), # E-1
    "prev_track"                : Note(17), # F-1
    "next_track"                : Note(18), # F#-1
    "last_track"                : Note(19), # G-1

    "scene_bank_to_selected"    : Note(24), # C0
    "scene_bank_to_playing_LC"  : Note(25), # C#0

    "scene_bank_first"          : Note(28), # E0
    "scene_bank_up"             : Note(29), # F0
    "scene_bank_down"           : Note(30), # F#0
    "scene_bank_last"           : Note(31), # G0

    "select_playing_LC_scene"   : Note(36), # C1
    "select_playing_DNAV_scene" : Note(37), # C#1

    "set_NAV_clips_enable"      : Note(40), # E1
    "set_DNAV_clips_enable"     : Note(41), # F1
    "set_DCUE_clips_enable"     : Note(42), # F#1
}

# Track Names for custom automation tracks
CLICK_TRACK          = "CLICK"
LAUNCH_CONTROL_TRACK = "LC"
NAVIGATION_TRACK     = "NAV"
DYNAMIC_NAV_TRACK    = "DNAV"
DYNAMIC_CUE_TRACK    = "DCUE"
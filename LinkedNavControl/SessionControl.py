import Live
import MIDI
import settings
from Logging import log

from Control import Control

class SessionControl(Control):
#    __module__ = __name__
    __doc__ = "Session parameters of NavControl"
    
    def __init__(self, c_instance, nav_controller):
        log("SessionControl::__init__")
        Control.__init__(self, c_instance, nav_controller)
        
    
    def get_midi_bindings(self):
        return (
            ("stop_playing", self.stop_playing),
            ("stop_all_clips", self.stop_all_clips),
            ("stop_all_clips_immediately", self.stop_all_clips_immediately),

            ("first_scene", self.select_first_scene),
            ("prev_scene", lambda value, mode, status:
                self.scroll_scenes(
                    -1,
                    MIDI.RELATIVE_TWO_COMPLIMENT,
                    MIDI.CC_STATUS)),
            ("next_scene", lambda value, mode, status:
                self.scroll_scenes(
                    1,
                    MIDI.RELATIVE_TWO_COMPLIMENT,
                    MIDI.CC_STATUS)),
            ("last_scene", self.select_last_scene),
            
            
            ("play_selected_scene", self.fire_selected_scene),
            ("play_prev_scene", self.fire_previous_scene),
            ("play_next_scene", self.fire_next_scene),
            ("select_playing_clip", self.select_playing_clip),
            
            
            ("stop_selected_track", self.stop_selected_track),
            ("mute_selected_track", self.mute_selected_track),
            ("unmute_selected_track", self.unmute_selected_track),
            

            ("first_track", self.select_first_track),
            ("prev_track", lambda value, mode, status:
                self.scroll_tracks(
                    -1,
                    MIDI.RELATIVE_TWO_COMPLIMENT,
                    MIDI.CC_STATUS)),
            ("next_track", lambda value, mode, status: 
                self.scroll_tracks(
                    1,
                    MIDI.RELATIVE_TWO_COMPLIMENT,
                    MIDI.CC_STATUS)),
            ("last_track", self.select_last_track),
            
            
            ("scene_bank_first", self.scene_bank_first),
            ("scene_bank_up", self.scene_bank_up),
            ("scene_bank_down", self.scene_bank_down),
            ("scene_bank_last", self.scene_bank_last),

            ("scene_bank_to_selected", self.scene_bank_to_selected),
            
            ("scroll_scenes", self.scroll_scenes),
            ("scroll_tracks", self.scroll_tracks),
            ("select_scene", self.select_scene),
            ("select_track", self.select_track),
        )
    
    # helper function 
    def get_all_tracks(self, only_visible = False):
        tracks = []
        for track in self.song.tracks:
            if not only_visible or track.is_visible:
                tracks.append(track)
                
        for track in self.song.return_tracks:
            tracks.append(track)
        tracks.append(self.song.master_track)
        return tracks
        
    
    # helper function to go from one track to the other
    def get_track_by_delta(self, track, d_value):
        tracks = self.get_all_tracks(only_visible = True)
        max_tracks = len(tracks)
        for i in range(max_tracks):
            if track == tracks[i]:
                return tracks[max((0, min(i+d_value, max_tracks-1)))]
    
    # helper function to go from one scene to the other
    def get_scene_by_delta(self, scene, d_value):
        scenes = self.song.scenes
        max_scenes = len(scenes)
        for i in range(max_scenes):
            if scene == scenes[i]:
                return scenes[max((0, min(i+d_value, max_scenes-1)))]


    def stop_playing(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:
            # ignore 0 values from CC-pads
            return
        self.song.stop_playing()


    def stop_all_clips(self, value, mode, status):
        self.song.stop_all_clips()


    def stop_all_clips_immediately(self, value, mode, status):
        self.song.stop_all_clips(False)
        self.song.stop_playing()


    def scroll_scenes(self, value, mode, status):
        if mode == MIDI.ABSOLUTE:
            # Invert value (127-value), somehow feels more natural 
            #   to turn left to go fully down and right to go up.
            # Also when assigning this to a fader this is 
            #   more natural as up is up and down is down.
            index = int((127-value)/(128.0/len(self.song.scenes)))
            self.song.view.selected_scene = self.song.scenes[index]
        else:
            self.song.view.selected_scene \
                = self.get_scene_by_delta(self.song.view.selected_scene, value)


    def select_scene(self, value, mode, status):
        scenes = self.song.scenes
        index = min(len(scenes)-1, value)
        self.song.view.selected_scene = scenes[index]
    
    
    def select_first_scene(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:
            return
        self.song.view.selected_scene = self.song.scenes[0]


    def select_last_scene(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:
            return
        self.song.view.selected_scene \
            = self.song.scenes[len(self.song.scenes)-1]


    def fire_selected_scene(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:
            return
        self.song.view.selected_scene.fire()


    def fire_previous_scene(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:
            return
        scene = self.get_scene_by_delta(self.song.view.selected_scene, -1)
        scene.fire()
        self.song.view.selected_scene = scene


    def fire_next_scene(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:
            return
        scene = self.get_scene_by_delta(self.song.view.selected_scene, 1)
        scene.fire()
        self.song.view.selected_scene = scene


    def select_playing_clip(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:
            return
        
        for clip_slot in self.song.view.selected_track.clip_slots:
            if clip_slot.has_clip and clip_slot.clip.is_playing:
                self.song.view.highlighted_clip_slot = clip_slot
    
    
    def scroll_tracks(self, value, mode, status):
        if mode == MIDI.ABSOLUTE:
            tracks = self.get_all_tracks(only_visible = True)
            index = int(value/(128.0/len(tracks)))
            self.song.view.selected_track = tracks[index]
        else:
            self.song.view.selected_track \
                = self.get_track_by_delta(self.song.view.selected_track, value)
    
    
    def select_track(self, value, mode, status):
        tracks = self.song.tracks
        index = min(len(tracks)-1, value)
        self.song.view.selected_track = tracks[index]

    
    def select_first_track(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:
            return
        tracks = self.song.tracks
        if self.song.view.selected_track == self.song.master_track:
            self.song.view.selected_track = tracks[len(tracks)-1]
        else:
            self.song.view.selected_track = tracks[0]
    
    
    def select_last_track(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:
            return
        if self.song.view.selected_track == self.song.master_track:
            return
        
        tracks = self.song.tracks
        # mimics Live's behavior: if last track is selected, select master
        if self.song.view.selected_track == tracks[len(tracks)-1]:
            self.song.view.selected_track = self.song.master_track
        else:
            self.song.view.selected_track = tracks[len(tracks)-1]


    def stop_selected_track(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:
            return
        self.song.view.selected_track.stop_all_clips()


    def mute_selected_track(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:
            return
        log("SessionControl::mute_selected_track")
        self.song.view.selected_track.mute = True


    def unmute_selected_track(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:
            return
        log("SessionControl::unmute_selected_track")
        self.song.view.selected_track.mute = False


    # Scene Bank Controls for Linked SessionControl

    def scene_bank_to_selected(self, value, mode, status):
        if not self.session:
            return
        track_offset = self.session.track_offset()
        scene = self.song.view.selected_scene
        scenes = self.song.scenes
        max_scenes = len(scenes)
        for i in range(max_scenes):
            if scene == scenes[i]:
                self.session.set_offsets(track_offset, i)


    def scene_bank_first(self, value, mode, status):
        if not self.session:
            return
        track_offset = self.session.track_offset()
        self.session.set_offsets(track_offset, 0)


    def scene_bank_up(self, value, mode, status):
        if not self.session:
            return
        track_offset = self.session.track_offset()
        scene_offset = self.session.scene_offset()
        if scene_offset > 0:
            new_scene_offset = max(0, scene_offset - 1)
            self.session.set_offsets(track_offset, new_scene_offset)


    def scene_bank_down(self, value, mode, status):
        if not self.session:
            return
        track_offset = self.session.track_offset()
        scene_offset = self.session.scene_offset()
        scenes = self.song.scenes
        max_scenes = len(scenes)
        if scene_offset < max_scenes:
            new_scene_offset = min(max_scenes, scene_offset + 1)
            self.session.set_offsets(track_offset, new_scene_offset)


    def scene_bank_last(self, value, mode, status):
        if not self.session:
            return
        track_offset = self.session.track_offset()
        scenes = self.song.scenes
        max_scenes = len(scenes) - 1
        self.session.set_offsets(track_offset, max_scenes)


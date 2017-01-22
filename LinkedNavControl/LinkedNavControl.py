from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.TransportComponent import TransportComponent
from _Framework.SessionComponent import SessionComponent

from Logging import log
import settings
import MIDI
from SessionControl import SessionControl

class LinkedNavControl(ControlSurface):

	def __init__(self, c_instance):
		log("LinkedNavControl::__init__")
		super(LinkedNavControl, self).__init__(c_instance)
		self.c_instance = c_instance
		# Set up internal objects
		with self.component_guard():
			self._setup_transport()
			self._setup_session()

		# mappings for registered MIDI notes/CCs
		self.midi_callbacks = {}
		# lookup object for fast lookup of cc to mode
		self.midi_cc_to_mode = {}
		
		# parse midi_mapping recursive for MIDI.CC
		self.mapping_parse_recursive(settings.midi_mapping.values())

		self._sessionControl = SessionControl(c_instance, self)



	def mapping_parse_recursive(self, mapping):
		tuple_type = type((1,2));
		for command in mapping:
			if type(command) == tuple_type:
				self.mapping_parse_recursive(command)
			elif isinstance(command, MIDI.CC):
				#log("MIDI CC %d is %s" % (command.key, command.mode))
				self.midi_cc_to_mode[command.key] = command.mode


	def suggest_map_mode(self, cc_no):
		#log("suggest_map_mode")
		if cc_no in self.midi_cc_to_mode:
			return self.midi_cc_to_mode[cc_no]
		return MIDI.ABSOLUTE # see MIDI.py for definitions of modes
	
	
	def refresh_state(self):
		#log("refresh_state")
		#for c in self.components:
		#	c.refresh_state()
		pass
	
	def update_display(self):
		#log("update_display")
		#for c in self.components:
		#	c.update_display()
		pass
	
	def connect_script_instances(self, instanciated_scripts):
		#log("connect_script_instances")
		pass


	# called from Live to build the MIDI bindings
	def build_midi_map(self, midi_map_handle):
		#log("build_midi_map")
		script_handle = self.c_instance.handle()
		
		for channel in range(16):
			callbacks = self.midi_callbacks.get(channel, {})
			
			for note in callbacks.get(MIDI.NOTEON_STATUS,{}).keys():
				#log("forward_midi_note is %s" % (str(note)))
				Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, channel, note)
			
			for cc in callbacks.get(MIDI.CC_STATUS,{}).keys():
				#log("forward_midi_cc is %s" % (str(cc)))
				Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, channel, cc)
	

	# called from Live when MIDI messages are received
	def receive_midi(self, midi_bytes):
		channel = (midi_bytes[0] & MIDI.CHAN_MASK)
		status  = (midi_bytes[0] & MIDI.STATUS_MASK)
		key     = midi_bytes[1]
		value   = midi_bytes[2]
		
		#log("receive_midi on channel %d, status %d, key %d, value %d" % (channel, status, key, value))
		
		# execute callbacks that are registered for this event
		callbacks = self.midi_callbacks.get(channel,{}).get(status,{}).get(key,[])
		mode = MIDI.ABSOLUTE
		if status == MIDI.CC_STATUS:
			# get mode and calculate signed int for MIDI value
			mode = self.suggest_map_mode(key)
			value = MIDI.relative_to_signed_int[mode](value)
		
		for callback in callbacks:
			callback(value, mode, status)
	

	# internal method to register callbacks from different controls
	def register_midi_callback(self, callback, key, mode, status, channel):
		if not channel in self.midi_callbacks:
			self.midi_callbacks[channel] = {}
		
		if not status in self.midi_callbacks[channel]:
			self.midi_callbacks[channel][status] = {
				key: [callback,]
			}
		else:
			if key in self.midi_callbacks[channel][status]:
				self.midi_callbacks[channel][status][key].append(callback)
			else:
				self.midi_callbacks[channel][status][key] = [callback, ]


	""" ================================================= """

	def _setup_transport(self):
		self._transport = TransportComponent()
		

	def _setup_session(self):
		self._session = SessionComponent(settings.numTRACKS, settings.numSCENES)
		self._session.name = "Session_Control"
		self.set_highlighting_session_component(self._session)
		self._session._link()
		

	def session(self):
		return self._session

	""" ================================================= """


	def suggest_input_port(self):
		return str('loopMIDI Port')


	def disconnect(self):
		log("LinkedNavControl::disconnect")
		if self._session and self._session._is_linked():
			self._session._unlink()
		super(LinkedNavControl, self).disconnect()

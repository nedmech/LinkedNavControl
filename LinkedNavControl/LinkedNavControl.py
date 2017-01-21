from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.TransportComponent import TransportComponent
from _Framework.SessionComponent import SessionComponent

from settings import *

class LinkedNavControl(ControlSurface):

	def __init__(self, c_instance):
		super(LinkedNavControl, self).__init__(c_instance)
		with self.component_guard():
			self._create_buttons()
			self._setup_transport()
			self._setup_session()
			self._map_controls()


	def _create_buttons(self):
		pass

	def _setup_transport(self):
		self._transport = TransportComponent()

	def _setup_session(self):
		self._session = SessionComponent(numTRACKS, numSCENES)
		self._session.name = "Session_Control"
		buttonUP = ButtonElement(True, MIDI_NOTE_TYPE, CHAN, SCENE_BANK_PREV)
		buttonDN = ButtonElement(True, MIDI_NOTE_TYPE, CHAN, SCENE_BANK_NEXT)
		self._session.set_scene_bank_buttons(buttonDN, buttonUP)
		self.set_highlighting_session_component(self._session)
		self._session._link()


	def _map_controls(self):
		pass


	def disconnect(self):
		if self._session and self._session._is_linked():
			self._session._unlink()
		super(LinkedNavControl, self).disconnect()

from _Framework.SessionComponent import SessionComponent
from Launchpad_MK2 import Launchpad_MK2

class LinkedLaunchpadMK2(Launchpad_MK2):
	# Get the SessionComponent to add it to linked sessions
	def _register_component(self, component):
		Launchpad_MK2._register_component(self, component)
		if isinstance(component, SessionComponent):
			self.session = component
			self.session._link()
		return None

	def disconnect(self):
		if self.session and self.session._is_linked():
			self.session._unlink()
		Launchpad_MK2.disconnect(self)

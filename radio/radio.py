import pygst
pygst.require('0.10')
import gst

class RadioPlayer(object):
	"""docstring for RadioPlayer"""
	def __init__(self):
		self.pipeline = gst.Pipeline("RadioPipe")
		self.player = gst.element_factory_make("playbin2", "player")

		if (not self.pipeline or not self.player):
			print 'Not all elements could be created. Cannot create a Gstreamer pipeline to stream radio...'
			exit(-1)

		self.pipeline.add(self.player)

		bus = self.pipeline.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self.on_message)


	def play_station(self, radioStation):
		self.player.set_property('uri', radioStation)
		self.pipeline.set_state(gst.STATE_PLAYING)
		# getting the bus

	def on_message(self, bus, message):
		if message.type == gst.MessageType.EOS:
			print message
		elif message.type == gst.MessageType.ERROR:
			error_msg = message.parse_error()
			print error_msg
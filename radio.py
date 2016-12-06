import gst
import json

class RadioPlayer():
	"""docstring for RadioPlayer"""
	def __init__(self):
		print "Creating radio player..."
		self.pipeline = gst.Pipeline("RadioPipe")
		self.player = gst.element_factory_make("playbin2", "player")

        # json configuration file which holds the radio stations url
		self.radio_stations_file = 'radio_stations.json'

		if (not self.pipeline or not self.player):
			print 'Not all elements could be created. Cannot create a Gstreamer pipeline to stream radio...'
			exit(-1)

		self.pipeline.add(self.player)
		print "Created GStreamer pipeline..."

		bus = self.player.get_bus()
		bus.enable_sync_message_emission()
		bus.add_signal_watch()
		# message::tag should give us only the tags
		bus.connect("message", self.on_tag_message)
		#bus.connect("message", self.on_message)

		#load radio stations
		with open(self.radio_stations_file) as file_stations:
			self.stations = json.load(file_stations)

		print "Loaded radio stations file..."
		self.radio_stations = self.stations['radio_stations']


	def play_station(self, radio):
		self.stop_any_station()
		print "{} is about to be played...".format(radio)
		self.player.set_property('uri', self.radio_stations[radio])
		self.pipeline.set_state(gst.STATE_PLAYING)
		# getting the bus

	def stop_any_station(self):
		self.pipeline.set_state(gst.STATE_READY)

	def get_stations(self):
		return self.radio_stations

	def on_tag_message(self, bus, message):
		#print message
		taglist = message.parse_tag()
		print taglist


	def on_message(self, bus, message):
		if message.type == gst.MessageType.EOS:
			print message
		elif message.type == gst.MessageType.ERROR:
			error_msg = message.parse_error()
			print error_msg
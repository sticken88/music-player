import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init(None)

import json

class RadioPlayer():
	"""docstring for RadioPlayer"""
	def __init__(self):
		print "Creating radio player..."
		#self.pipeline = gst.Pipeline("RadioPipe")
		self.player = Gst.ElementFactory.make("playbin", "player")
		# set the initial default value to 0.5
		self.player.set_property('volume', 0.5)

        # json configuration file which holds the radio stations url
		self.radio_stations_file = 'radio_stations.json'

		if (not self.player):
			print 'Not all elements could be created. Cannot create a Gstreamer pipeline to stream radio...'
			exit(-1)

		#self.pipeline.add(self.player)
		print "Created GStreamer playbin..."
		print "Default volume set to 0.5"

		bus = self.player.get_bus()
		#bus.enable_sync_message_emission()
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
		#self.pipeline.set_state(gst.STATE_PLAYING)
		self.player.set_state(Gst.State.PLAYING)


	def set_volume(self, volume):
		print "New volume set {}".format(volume)
		self.player.set_property('volume', volume)

	
	def stop_any_station(self):
		#self.pipeline.set_state(gst.STATE_READY)
		self.player.set_state(Gst.State.READY)

	
	def get_stations(self):
		return self.radio_stations

	
	def on_tag_message(self, bus, message):
		print "on tag message called..."
		#print message
		# taglist = message.parse_tag()
		# print taglist


	def on_message(self, bus, message):
		if message.type == gst.MessageType.EOS:
			print message
		elif message.type == gst.MessageType.ERROR:
			error_msg = message.parse_error()
			print error_msg
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
from PyQt4.QtCore import QObject

from gi.repository import Gst
import json

class RadioPlayer(QObject):
	"""docstring for RadioPlayer"""
	def __init__(self):
		QObject.__init__(self)
		Gst.init(None) # maybe it's not needed since it's already called

		self.radio = Gst.ElementFactory.make("playbin", "player")

		if not self.radio:
			print 'Not all elements could be created. Cannot create a Gstreamer pipeline to stream radio...'
			exit(-1)

        # set the initial default value to 0.5
		self.radio.set_property('volume', 0.5)
		print "Created GStreamer pipeline to stream radio..."

		bus = self.radio.get_bus()
		#bus.enable_sync_message_emission()
		bus.add_signal_watch()
		# message::tag should give us only the tags
		bus.connect("message", self.on_message)

		self.load_radio_stations()


	def play_station(self, radio):
		self.radio.set_property('uri', self.radio_stations[radio])
		self.radio.set_state(Gst.State.PLAYING)


	def load_radio_stations(self):
		# json configuration file which holds the radio stations url
		self.radio_stations_file = './radio/radio_stations.json'

		#load radio stations
		with open(self.radio_stations_file) as file_stations:
		    self.stations = json.load(file_stations)

		print "Loaded radio stations file..."
		self.radio_stations = self.stations['radio_stations']


	def on_message(self, bus, message):
		#print message.type
		if message.type == Gst.MessageType.ERROR:
		   error_msg = message.parse_error()
		   print error_msg

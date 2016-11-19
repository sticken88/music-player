import gst
import time

class MusicPlayer():

   def __init__(self):

      # flag used to switch between play and pause
      self.playing = False
      # Create a Gstreamer pipeline
      self.pipeline = gst.Pipeline('pipeline')

      # Create the elements that will be added to the pipeline
      self.audio_source = gst.element_factory_make('filesrc', 'audio_source')
      self.decode = gst.element_factory_make('mad', 'decode')
      self.convert = gst.element_factory_make('audioconvert', 'convert')
      self.equalizer = gst.element_factory_make('equalizer-3bands', 'equalizer')
      self.audio_sink = gst.element_factory_make('autoaudiosink', 'audio_sink')
      self.volume = gst.element_factory_make('volume')
      self.volume.set_property('volume', 0.5)

      # Ensure all elements were created successfully.
      if (not self.pipeline or not self.audio_source or not self.decode or 
          not self.convert or not self.equalizer or not self.audio_sink or
          not self.volume):
            print 'Not all elements could be created. Cannot create a Gstreamer pipeline'
            exit(-1)

      # Setting equalizer prpoperties
      #self.equalizer.set_property('band1', -24.0)
      #self.equalizer.set_property('band2', -24.0)

      self.pipeline.add(self.audio_source, self.decode, self.convert, self.equalizer, self.audio_sink, self.volume)

      # Add our elements to the pipeline
      if (not gst.element_link_many(self.audio_source, self.decode, self.convert, self.volume,
          self.equalizer, self.audio_sink)):
            print "Elements could not be linked."
            exit(-1)

      # manage the bus (not sure if it's the right place)
      bus = self.pipeline.get_bus()
      bus.add_signal_watch()
      bus.connect("message", self.on_message)

      '''msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,
            gst.MESSAGE_ERROR | gst.MESSAGE_EOS)
      print msg'''
      #gst_bus_add_watch (bus, my_bus_callback, NULL);


   def load_audio(self, audioResource):
      self.current_song = audioResource
      self.stop_audio()
      self.audio_source.set_property('location', audioResource)
      self.play_audio()


   def play_audio(self):
      # Play the song
      self.pipeline.set_state(gst.STATE_PLAYING)
      self.playing = True
      print "Play the stream.."


      '''self.bus = self.pipeline.get_bus()

      self.msg = self.bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,
                  gst.MESSAGE_ERROR | gst.MESSAGE_EOS)'''

   
   def pause_audio(self):
      self.pipeline.set_state(gst.STATE_PAUSED)
      self.playing = False
      print "Pausing the stream.."


   def stop_audio(self):
      self.pipeline.set_state(gst.STATE_READY)
      self.playing = False
      print "Stopping the stream.."


   def play_pause_audio(self):
       if self.playing:
           self.pause_audio()
       else:
           self.play_audio()

   def reload_audio(self):
       self.load_audio(self.current_song)

   def set_volume(self, volume):
       self.volume.set_property('volume', volume)


   def on_message(self, bus, message):

      if message.type == gst.MessageType.EOS:
         #self.pipeline.set_state(gst.STATE_READY)
         print message
      elif message.type == gst.MessageType.ERROR:
         error_msg = message.parse_error()
         #self.pipeline.set_state(gst.STATE_NULL)
         print error_msg
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import os

# module to handle audio files
from kivy.core.audio import SoundLoader

# class used to show a file system manager to choose a song to play
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MusicPlayer(FloatLayout):

    loadfile = ObjectProperty(None)
   
    ''' Shows the popup to choose the file to play
    '''
    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, path, filename):
        self.song = SoundLoader.load(filename[0])
        self.elapsed = 0
        # It seems to be a reasonable value for now
        self.song.volume = 0.3
        print "Loaded {}".format(filename[0])
        self.dismiss_popup()

    def __init__(self, **kwargs):
       super(MusicPlayer, self).__init__(**kwargs)
      
    '''Playing or pausing a song.
        1) If stopped play it again from the 'elapsed' value.
           If it's 0 play it from the beginning.
        2) If it's playing store the elapsed time and stop the song.
    '''
    def play_pause_song(self):

       if self.song.state == 'stop':
          print "Play or resume"
          self.song.play()
          self.song.seek(self.elapsed)
       elif self.song.state == 'play':
          print "Stopping.."
          self.elapsed = self.song.get_pos()
          self.song.stop()

    ''' Stopping the song.
        1) self.elapsed set to 0 so the next song (or the same)
           will be played from the beginning
        2) actually stop the song
    '''    
    def stop_song(self):
       self.elapsed = 0
       self.song.stop()

    ''' Reloading the song if it's currently playing.
        Just call self.stop_song and then self.play_pause_song        
    '''
    def reload_song(self):
       if self.song.state == 'play':
          self.stop_song()
          self.play_pause_song()

    ''' Setting the volume.
        When the value of the slider is changed, this will affect the 
        volume of the played song.
    '''
    def set_volume(self, value):
       self.song.volume = value
       

class TestApp(App):
    def build(self):
        return MusicPlayer()

Factory.register('TestApp', cls=TestApp)
Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == "__main__":
    TestApp().run()

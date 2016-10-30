from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import os

# module to handle audio files
from music_player import MusicPlayer

# class used to show a file system manager to choose a song to play
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MainGui(FloatLayout):

    loadfile = ObjectProperty(None)
    playing = False
   
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
        self.player.load_audio(filename[0])
        self.dismiss_popup()

    def __init__(self, **kwargs):
       super(MainGui, self).__init__(**kwargs)
       self.player = MusicPlayer()
      
    '''Playing or pausing a song.
        1) If stopped play it again from the 'elapsed' value.
           If it's 0 play it from the beginning.
        2) If it's playing store the elapsed time and stop the song.
    '''
    def play_pause_audio(self):
       if self.playing:
           self.pause_audio()
       else:
           self.play_audio()


    def pause_audio(self):
       self.playing = False
       self.player.pause_audio()       


    def play_audio(self):
       self.playing = True
       self.player.play_audio()
       # TODO: to be fully tested
       #self.player.look_bus()

    ''' Stopping the song.
        1) self.elapsed set to 0 so the next song (or the same)
           will be played from the beginning
        2) actually stop the song
    '''    
    def stop_audio(self):
       self.playing = False
       self.player.stop_audio()
 
    ''' Reloading the song if it's currently playing.
        Just call self.stop_song and then self.play_pause_song        
    '''
    def reload_song(self):
       self.player.reload_song()

    ''' Setting the volume.
        When the value of the slider is changed, this will affect the 
        volume of the played song.
    '''
    def set_volume(self, value):
       self.set_volume(value)


class TestApp(App):
    def build(self):
        return MainGui()

Factory.register('TestApp', cls=TestApp)
Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == "__main__":
    TestApp().run()

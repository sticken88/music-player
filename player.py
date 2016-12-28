import pygst
pygst.require('0.10')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.label import Label

import os

# module to handle audio files
from music_player import MusicPlayer
from radio import RadioPlayer
from library_manager import LibraryManager

# class used to show a file system manager to choose a song to play
'''class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)'''

class MainGui(BoxLayout):
    # ScreenManager that will be used to change between the two screens
    sm = ObjectProperty()
    def __init__(self, **kwargs):
       super(MainGui, self).__init__(**kwargs)

       # Just prepare the screen manager
       self.sm.add_widget(MusicScreen(name='MusicScreen'))
       self.sm.add_widget(RadioScreen(name='RadioScreen'))
       self.sm.current = "MusicScreen"

    def switch_screen(self, args):
      self.sm.current = "{}Screen".format(args[1])
      print "Switching to '{}' screen...".format(args[1])


class RadioScreen(Screen):

    def __init__(self, **kwargs):
       super(RadioScreen, self).__init__(**kwargs)
       self.radio_player = RadioPlayer()

       # # Getting the layout to dinamically add the buttons
       rs_layout = self.ids.rs_layout

       # getting the radio stations data
       stations = self.radio_player.get_stations()

       for radio in stations:
          btn = Button(text=radio)# , on_press=self.play_station(radio)
          #btn.bind(on_press=self.pressed)
          btn.bind(on_press=self.play_station)
          rs_layout.add_widget(btn)

       print "Radio Screen created"

    def play_station(self, instance):
      # getting the text from the button
      radio = instance.text
      print "Station that must be played: {}".format(radio)
      self.radio_player.play_station(radio)


    def set_volume(self, volume):
      self.radio_player.set_volume(volume)



class MusicScreen(Screen):

    ''' Shows the popup to choose the file to play
    '''
    '''def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()'''

    def __init__(self, **kwargs):
       super(MusicScreen, self).__init__(**kwargs)
       self.library_manager = LibraryManager()
       self.player = MusicPlayer()

       # # Getting the layout to dinamically add the buttons
       ml_list_view = self.ids.ml_list_view

       # adding files to library
       songs = self.library_manager.parse_library()

       # for song in songs:
       #    btn = Button(text=os.path.basename(song), font_size=14)# , on_press=self.play_station(radio)
       #    #btn.bind(on_press=self.pressed)
       #    #btn.bind(on_press=self.play_station)
       #    ml_layout.add_widget(btn)

       list_adapter = ListAdapter(data=songs, cls=ListItemButton, selection_mode='single')
       list_adapter.bind(on_selection_change=self.selection_change)

       ml_list_view.adapter = list_adapter

       # songs_text = ''
       # for song in songs:
       #     songs_text = songs_text + song

       # library_text.text = songs_text#''.join('aaaa ').join('bbbb')#, 'and something else')
       #library_text.text = library_text.text.join('bbbb')

    def selection_change(self, adapter, *args):
        print "selection changed"



    def load(self, path, filename):
        #self.player.stop_audio()
        self.player.load_audio(filename[0])
        #self.dismiss_popup()

      
    '''Playing or pausing a song.
        1) If stopped play it again from the 'elapsed' value.
           If it's 0 play it from the beginning.
        2) If it's playing store the elapsed time and stop the song.
    '''
    def play_pause_audio(self):
      self.player.play_pause_audio()


    def pause_audio(self):
       self.player.pause_audio()       


    def play_audio(self):
       self.player.play_audio()
       # TODO: to be fully tested
       #self.player.look_bus()

    ''' Stopping the song.
        1) self.elapsed set to 0 so the next song (or the same)
           will be played from the beginning
        2) actually stop the song
    '''    
    def stop_audio(self):
       self.player.stop_audio()
 
    ''' Reloading the song if it's currently playing.
        Just call self.stop_song and then self.play_pause_song        
    '''
    def reload_audio(self):
       self.player.reload_audio()

    ''' Setting the volume.
        When the value of the slider is changed, this will affect the 
        volume of the played song.
    '''
    def set_volume(self, value):
       self.player.set_volume(value)


class TestApp(App):
    def build(self):
        return MainGui()

Factory.register('TestApp', cls=TestApp)
#Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == "__main__":
    TestApp().run()

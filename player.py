from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider

# module to handle audio files
from kivy.core.audio import SoundLoader

class MusicPlayer(GridLayout):

    play = False
    song = None
    elapsed = 0

    def __init__(self, **kwargs):
       super(MusicPlayer, self).__init__(**kwargs)
       self.cols = 2
       self.row = 2
       self.play_pause = Button(text='Play/Pause')
       self.play_pause.bind(on_press=self.play_pause_song)
       self.add_widget(self.play_pause)

       self.stop = Button(text='Stop')
       self.stop.bind(on_press=self.stop_song)
       self.add_widget(self.stop)

       self.volume_slider = Slider(min=0, max=1, step=0.01, value=0.5)
       self.volume_slider.bind(value=self.set_volume)
       self.add_widget(self.volume_slider)

       self.song = SoundLoader.load("/home/matteo/Music/Sigala_-_Sweet_Lovin_(Official_Audio)_mp3.mp3")
   
       # It seems to be a reasonable value for now
       self.song.volume = 0.3

       
    ''' Playing or pausing a song
        1) If stopped play it again from the 'elapsed' value.
           If it's 0 play it from the beginning.
        2) If it's playing store the elapsed time and stop the song.
    '''
    def play_pause_song(self, instance):

       if self.song.state == 'stop':
          print "Play or resume"
          self.song.play()
          self.song.seek(self.elapsed)
       elif self.song.state == 'play':
          print "Stopping.."
          self.elapsed = self.song.get_pos()
          self.song.stop()

    ''' Stopping the song
        1) self.elapsed set to 0 so the next song (or the same)
           will be played from the beginning
        2) actually stop the song
    '''    
    def stop_song(self, instance):
       self.elapsed = 0
       self.song.stop()

    def set_volume(self, instance, value):
       self.song.volume = value
       #print self.value
       

class TestApp(App):
    def build(self):
        return MusicPlayer()

if __name__ == '__main__':
    TestApp().run()

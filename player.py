from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

# module to handle audio files
from kivy.core.audio import SoundLoader

class MusicPlayer(GridLayout):

    def __init__(self, **kwargs):
       super(MusicPlayer, self).__init__(**kwargs)
       self.song = SoundLoader.load("/home/matteo/Music/Sigala_-_Sweet_Lovin_(Official_Audio)_mp3.mp3")
       self.elapsed = 0
       # It seems to be a reasonable value for now
       self.song.volume = 0.3
      
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

    ''' Setting the volume.
        When the value of the slider is changed, this will affect the 
        volume of the played song.
    '''
    def set_volume(self, value):
       self.song.volume = value
       

class TestApp(App):
    def build(self):
        return MusicPlayer()

if __name__ == "__main__":
    TestApp().run()

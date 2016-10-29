import os
from kivy.core.audio import SoundLoader # to handle audio files

class MusicPlayer():

    def __init__(self):
        self.volume = 0.5
        self.elapsed = 0
        self.song = None

    def load_song(self, title):
        self.song = SoundLoader.load(title)
        # It seems to be a reasonable value for now
        self.song.volume = self.volume
        print "Loaded {}".format(title)


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
    def set_volume(self, volume):
       self.volume = volume
       self.song.volume = self.volume

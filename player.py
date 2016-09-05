from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

# module to handle audio files
from kivy.core.audio import SoundLoader

class MusicPlayer(GridLayout):

    play = False
    song = None

    def __init__(self, **kwargs):
       super(MusicPlayer, self).__init__(**kwargs)
       self.cols = 1
       self.row = 1
       self.play_stop = Button(text='Play/Stop')
       self.play_stop.bind(on_press=self.play_stop_song)
       self.add_widget(self.play_stop)

       self.song = SoundLoader.load("/home/matteo/Music/Sigala_-_Sweet_Lovin_(Official_Audio)_mp3.mp3")
       

    def play_stop_song(self, instance):
       print "button toggled"
       self.play = not self.play

       self.song.play() if self.play else self.song.stop()
       


class TestApp(App):
    def build(self):
        return MusicPlayer()
        '''sound = SoundLoader.load("/home/matteo/Music/Sigala_-_Sweet_Lovin_(Official_Audio)_mp3.mp3")

        if sound:
           print "Sound found at %s" % (sound.source)
           print "Sound is %.3f seconds" % (sound.length)
           print str(type(sound))
           #sound.play()

        return Button(text='Hello World')'''

if __name__ == '__main__':
    TestApp().run()

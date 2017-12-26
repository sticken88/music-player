import sys, os
from gi.repository import GObject
'''import gobject, pygst
pygst.require('0.10')
import gst'''

from backend import MusicPlayer

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QApplication, QMainWindow, QPushButton, \
                         QFileDialog, QListView, QListWidgetItem

Ui_MainWindow, QtBaseClass = uic.loadUiType('frontend.ui')

# define a custom QWidget class used to model the i-th widget
# reference: https://stackoverflow.com/questions/25187444/pyqt-qlistwidget-custom-items
class CustomQWidget (QtGui.QWidget):
    # string to hold the path of the song
    media_path = ""

    def __init__ (self, parent = None):
        super(CustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtGui.QVBoxLayout()
        self.textArtistQLabel    = QtGui.QLabel()
        self.textTitleQLabel  = QtGui.QLabel()
        self.textQVBoxLayout.addWidget(self.textArtistQLabel)
        self.textQVBoxLayout.addWidget(self.textTitleQLabel)
        #self.allQHBoxLayout  = QtGui.QHBoxLayout()
        #self.iconQLabel      = QtGui.QLabel()
        #self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        #self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        #self.setLayout(self.allQHBoxLayout)
        self.setLayout(self.textQVBoxLayout)

    def set_artist_name(self, artist_name):
        self.textArtistQLabel.setText(artist_name)

    def set_song_title(self, song_title):
        self.textTitleQLabel.setText(song_title)

    def set_media_path(self, media_path):
        self.media_path = media_path

    def get_media_path(self):
        return self.media_path

# subclassing QListWidgetItem to hold the path of the media
class CustomQListWidgetItem(QListWidgetItem):
    def __init__(self, media_path, parent = None):
        super(CustomQListWidgetItem, self).__init__(parent)
        self.media_path = media_path

    # method to get the media path
    def get_media_path(self):
        return self.media_path


#class MainWindow(QMainWindow):
class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

     def __init__(self):
         QtGui.QMainWindow.__init__(self)
         Ui_MainWindow.__init__(self)
         self.setupUi(self)

         # set the default properties of the volume slider
         self.volumeSlider.setMinimum(0)
         self.volumeSlider.setMaximum(100)
         self.volumeSlider.setValue(50)
         self.volumeSlider.setTickInterval(1)

         # instantiate the MusicPlayer object
         self.player = MusicPlayer()

         # setting the methods to be called
         self.playButton.clicked.connect(self.playPauseAudio)
         self.stopButton.clicked.connect(self.stopAudio)
         self.browseButton.clicked.connect(self.browseFs)
         self.volumeSlider.valueChanged.connect(self.changeVolume)

         self.player.eosReached.connect(self.next_song)

         self.songsListWidget.itemDoubleClicked.connect(self.play_song)

         # Create a CustomQWidget for each item that must be added to the list
         songCustomWidget = CustomQWidget()
         songCustomWidget.set_artist_name("Giorgia")
         songCustomWidget.set_song_title("01 - Oronero.mp3")
         songCustomWidget.set_media_path("/home/matteo/Music/Giorgia - Oronero (2016)/01 - Oronero.mp3")

         customQListWidgetItem = CustomQListWidgetItem(songCustomWidget.get_media_path()) #QtGui.QListWidgetItem(self.songsListWidget)
         # Set size hint and media path
         customQListWidgetItem.setSizeHint(songCustomWidget.sizeHint())

         # Add QListWidgetItem into QListWidget
         self.songsListWidget.addItem(customQListWidgetItem)
         self.songsListWidget.setItemWidget(customQListWidgetItem, songCustomWidget)

         #self.setCentralWidget(self.songsListWidget)

         # dummy QListView example
         '''dummy_songs = []
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/01 - Oronero.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/02 - Danza.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/03 - Scelgo ancora te.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/04 - Credo.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/05 - Per non pensarti.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/06 - Vanita.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/07 - Posso farcela.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/08 - Come acrobati.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/09 - Mutevole.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/10 - Tolto e dato.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/11 - Amore quanto basta.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/12 - Sempre si cambia.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/13 - Grande Maestro.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/14 - Regina di notte.mp3")
         dummy_songs.append("/home/matteo/Music/Giorgia - Oronero (2016)/15 - Non fa niente.mp3")
         self.songsListWidget.addItems(dummy_songs)'''
         '''for i in range(10):
            item = QListWidgetItem("Song %i" % i)
            self.songsListWidget.addItem(item)'''

         #self.songsListWidget.show()


     def play_song(self, song):
         print "Selected {}".format(song.get_media_path())
         # Get the current index. It will be incremented later if needed
         self.currentSongIndex = self.songsListWidget.row(song)
         self.player.load_audio(song.get_media_path())
         self.playButton.setText('Pause')

     def next_song(self):
         # used to select the next song
         self.currentSongIndex += 1
         self.next_song = self.songsListWidget.item(self.currentSongIndex)
         self.player.load_audio(next_song.get_media_path())

     def playPauseAudio(self):
         self.player.play_pause_audio()
         if self.playButton.text() == 'Play':
             self.playButton.setText('Pause')
         else:
             self.playButton.setText('Play')


     def stopAudio(self):
         self.player.stop_audio()
         self.playButton.setText('Play')

     def changeVolume(self):
        self.player.set_volume(float(self.volumeSlider.value())/100)

     def browseFs(self):
         filepath = QFileDialog.getOpenFileName(self, 'Choose File')
         if filepath:
             self.player.load_audio(str(filepath))
         else:
            print "Cannot load any song.."

         '''if self.button.text() == 'Start':
             filepath = QFileDialog.getOpenFileName(self, 'Choose File')
             if filepath:
                 self.button.setText('Stop')
                 #self.player.set_property('uri', 'file://' + filepath)
                 self.player.load_audio(filepath)
                 #self.player.set_state(gst.STATE_PLAYING)
         else:
             #self.player.set_state(gst.STATE_NULL)
             self.player.stop_audio()
             self.button.setText('Start')'''
'''
     def on_message(self, bus, message):
         t = message.type
         if t == gst.MESSAGE_EOS:
             self.player.set_state(gst.STATE_NULL)
             self.button.setText('Start')
         elif t == gst.MESSAGE_ERROR:
             self.player.set_state(gst.STATE_NULL)
             err, debug = message.parse_error()
             print 'Error: %s' % err, debug
             self.button.setText('Start')
'''


if __name__ == '__main__':

     GObject.threads_init()
     qApp = QApplication(sys.argv)
     qApp.connect(qApp, SIGNAL('lastWindowClosed()'),
                  qApp, SLOT('quit()'))
     mainwindow = MainWindow()
     mainwindow.show()
     sys.exit(qApp.exec_())

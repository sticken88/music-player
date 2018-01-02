import sys
from gi.repository import GObject

# to walk the filesystem
from os import listdir, walk
from os.path import isfile, join, expanduser

# to play songs
from backend import MusicPlayer

# to hanlde the Qt GUI
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QApplication, QMainWindow, QPushButton, \
                         QFileDialog, QListView, QListWidgetItem, QIcon

Ui_MainWindow, QtBaseClass = uic.loadUiType('./gui/frontend.ui')

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

     music_path = ""
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

         self.player.eosReached.connect(self.play_next_song)

         self.songsListWidget.itemDoubleClicked.connect(self.play_song)

         # set icons for the button
         self.stopButton.setIcon(QtGui.QIcon('./icons/stop.png'))
         self.playButton.setIcon(QtGui.QIcon('./icons/play.png'))

         # set model in tree view
         self.build_file_system()

         # create music list
         self.populate_song_list()


     def build_file_system(self):
         self.music_root = expanduser("~") + "/Music"
         self.fs_model = QtGui.QFileSystemModel(self)
         self.fs_model.setRootPath(self.music_root)
         self.indexRoot = self.fs_model.index(self.fs_model.rootPath())

         self.fileSystemView.setModel(self.fs_model)
         self.fileSystemView.setRootIndex(self.indexRoot)


     def populate_song_list(self):
         # set basic variable used to visit the filesystem
         home = expanduser("~")
         music_path = join(home, "Music/")

         for current_dir, subdirs, files in walk(music_path):
             for file_song in files:
                full_path_file = join(current_dir, file_song)
                if isfile(full_path_file) and file_song.endswith('.mp3'):
                   # Create a CustomQWidget for each item that must be added to the list
                   songCustomWidget = CustomQWidget()
                   # TODO: properly extract artist name
                   songCustomWidget.set_artist_name("Unknown")
                   songCustomWidget.set_song_title(file_song)
                   songCustomWidget.set_media_path(full_path_file)

                   customQListWidgetItem = CustomQListWidgetItem(songCustomWidget.get_media_path()) #QtGui.QListWidgetItem(self.songsListWidget)
                   # Set size hint and media path
                   customQListWidgetItem.setSizeHint(songCustomWidget.sizeHint())

                   # Add QListWidgetItem into QListWidget
                   self.songsListWidget.addItem(customQListWidgetItem)
                   self.songsListWidget.setItemWidget(customQListWidgetItem, songCustomWidget)



     def play_song(self, song):
         print "Selected {}".format(song.get_media_path())
         # Get the current index. It will be incremented later if needed
         self.currentSongIndex = self.songsListWidget.row(song)
         self.player.load_audio(song.get_media_path())
         self.playButton.setText('Pause')
         self.playButton.setIcon(QtGui.QIcon('./icons/pause.png'))


     def play_next_song(self):
         # used to select the next song
         self.currentSongIndex += 1
         self.next_song = self.songsListWidget.item(self.currentSongIndex)
         print "Next song {}".format(self.next_song.get_media_path())
         self.player.load_audio(self.next_song.get_media_path())
         self.songsListWidget.setCurrentRow(self.currentSongIndex)


     def playPauseAudio(self):
         self.player.play_pause_audio()
         if self.playButton.text() == 'Play':
             self.playButton.setText('Pause')
             self.playButton.setIcon(QtGui.QIcon('./icons/pause.png'))
         else:
             self.playButton.setText('Play')
             self.playButton.setIcon(QtGui.QIcon('./icons/play.png'))


     def stopAudio(self):
         self.player.stop_audio()
         self.playButton.setText('Play')
         self.playButton.setIcon(QtGui.QIcon('./icons/play.png'))


     def changeVolume(self):
        self.player.set_volume(float(self.volumeSlider.value())/100)


     def browseFs(self):
         filepath = QFileDialog.getOpenFileName(self, 'Choose File')
         if filepath:
             self.player.load_audio(str(filepath))
         else:
            print "Cannot load any song.."


if __name__ == '__main__':

     GObject.threads_init()
     qApp = QApplication(sys.argv)
     qApp.connect(qApp, SIGNAL('lastWindowClosed()'),
                  qApp, SLOT('quit()'))
     mainwindow = MainWindow()
     mainwindow.show()
     sys.exit(qApp.exec_())

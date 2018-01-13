from PyQt4 import QtGui
from PyQt4.QtGui import QListWidgetItem

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

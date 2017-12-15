import sys, os
from gi.repository import GObject
'''import gobject, pygst
pygst.require('0.10')
import gst'''

from backend import MusicPlayer

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QApplication, QMainWindow, QPushButton, \
                         QFileDialog

Ui_MainWindow, QtBaseClass = uic.loadUiType('frontend.ui')
#class MainWindow(QMainWindow):
class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

     def __init__(self):
         QtGui.QMainWindow.__init__(self)
         Ui_MainWindow.__init__(self)
         self.setupUi(self)

         # instantiate the MusicPlayer object
         self.player = MusicPlayer()

         # setting the methods to be called
         self.playButton.clicked.connect(self.playPause)

         '''try:
             # alsasink pulsesink osssink autoaudiosink
             device = gst.parse_launch('alsasink')
         except gobject.GError:
             print 'Error: could not launch audio sink'
         else:
             self.player.set_property('audio-sink', device)'''
         '''self.bus = self.player.get_bus()
         self.bus.add_signal_watch()
         self.bus.connect('message', self.on_message)'''

     def playPause(self):
         print "Start Button pressed!!"
         #self.player.play_pause_audio()
         if self.playButton.text() == 'Play':
             self.playButton.setText('Pause')
         else:
             self.playButton.setText('Play')

     def start_stop(self):
         if self.button.text() == 'Start':
             filepath = QFileDialog.getOpenFileName(self, 'Choose File')
             if filepath:
                 self.button.setText('Stop')
                 #self.player.set_property('uri', 'file://' + filepath)
                 self.player.load_audio(filepath)
                 #self.player.set_state(gst.STATE_PLAYING)
         else:
             #self.player.set_state(gst.STATE_NULL)
             self.player.stop_audio()
             self.button.setText('Start')
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

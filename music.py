import sys, os
import gobject, pygst
pygst.require('0.10')
import gst
from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QApplication, QMainWindow, QPushButton, \
                         QFileDialog


class MainWindow(QMainWindow):
     def __init__(self):
         QMainWindow.__init__(self)
         self.setWindowTitle('Audio-Player')
         self.resize(120, 50)
         self.move(500, 500)
         self.button = QPushButton(self)
         self.button.setText('Start')
         self.button.setMinimumSize(90, 0)
         self.setCentralWidget(self.button)
         self.connect(self.button, SIGNAL('clicked()'), self.start_stop)
         self.player = gst.element_factory_make('playbin', 'player')
         try:
             # alsasink pulsesink osssink autoaudiosink
             device = gst.parse_launch('alsasink')
         except gobject.GError:
             print 'Error: could not launch audio sink'
         else:
             self.player.set_property('audio-sink', device)
             self.bus = self.player.get_bus()
             self.bus.add_signal_watch()
             self.bus.connect('message', self.on_message)

     def start_stop(self):
         if self.button.text() == 'Start':
             filepath = QFileDialog.getOpenFileName(self, 'Choose File')
             if filepath:
                 self.button.setText('Stop')
                 self.player.set_property('uri', 'file://' + filepath)
                 self.player.set_state(gst.STATE_PLAYING)
         else:
             self.player.set_state(gst.STATE_NULL)
             self.button.setText('Start')

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


if __name__ == '__main__':

     gobject.threads_init()
     qApp = QApplication(sys.argv)
     qApp.connect(qApp, SIGNAL('lastWindowClosed()'),
                  qApp, SLOT('quit()'))
     mainwindow = MainWindow()
     mainwindow.show()
     sys.exit(qApp.exec_())

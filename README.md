# music-player
I just want to create my own music player and radio streamer in python. I chosed to use kivy as development framework to build the GUI while GStreamer is used to handle the radio streaming and the songs

## Current Requirements
- Playing music
- Creating, modifying and reproducing playlists
- Radio Streaming

### TODO
- Improve the layout [Create two distinct screens with their own layouts]
- Integrate LibraryManager into the player
- Intregrate PlaylistManager into the player

### DONE
- Replaced kivy SoundLoader class with pure GStreamer in order to have a player indipendent from the GUI used.

## Dependencies
- GStreamer v0.1
- Kivy library installed for python 2. Instructions: https://kivy.org/docs/installation/installation-linux.html#ubuntu-11-10-or-newer

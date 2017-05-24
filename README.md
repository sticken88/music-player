# music-player
I just want to create my own music player and radio streamer in python. I chosed to use kivy as development framework to build the GUI while GStreamer is used to handle the radio streaming and the songs.

## Current Requirements
- Play local songs.
- Create, modify and reproduce playlists.
- Radio Streaming.

### TODO
- Identify a way to stop radio when a song starts to play and vice versa.

#### Music player
- Review LibraryManager.
- Review PlaylistManager.

#### Radio player
- Show metadata [e.g. song being played, radio talk, etc.].
- Resize buttons.
- Add 'Rec' button to record audio streams [?].

### DONE
- Replaced kivy SoundLoader class with pure GStreamer in order to have a player indipendent from the GUI used.
- Improved (a little bit) the layout [Created two distinct screens with their own layouts].

#### Music player
- Different audio formats are managed now [mp3 and m4a]. Rewritten the MusicPlayer class in order to use playbin which automatically handles multiple formats.

#### Radio player
- Added volume control.

## Dependencies
- GStreamer v0.1
- Kivy library installed for python 2. Instructions: https://kivy.org/docs/installation/installation-linux.html#ubuntu-11-10-or-newer

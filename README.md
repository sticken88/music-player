# music-player
Music player and radio streamer written in python that uses GStreamer as multimedia framework.
PyQt 4 is used to develop the GUI as of today but ideally other GUIs will be supported.

## Current Requirements
- Play local songs.
- Create, modify and reproduce playlists.
- Radio Streaming.

### TODO
- Implement slider with duration of the song
- Move the custom Song class to a different python module?
- Visit the filesystem to scan all the songs o just the current selected folder?
- Filter all the music format
- Properly separate modules [e.g list songs among others?]
- [music-player] review LibraryManager and PlaylistManager
- [radio-player] show metadata (e.g. song being played, radio talk, etc.) and add 'Rec' button to record audio streams [?]
- [POSTPONED] Identify a way to stop radio when a song starts to play and vice versa.
- [POSTPONED] Add comments to use doxygen or sphinx

## Dependencies
- PyQt 4 `sudo apt-get install python-qt4 python-qt4-dbus python-qt4-dev python-qt4-doc`
- GStreamer 1.0, see [the official documentation](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html)

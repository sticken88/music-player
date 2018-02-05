# to walk the filesystem
import os
from os import walk
from os.path import join

class PlaylistManager():

   playlist_path = join("./", "playlists/")


   def get_playlists(self):
      # create the playlists folder if missing
      if not os.path.exists(self.playlist_path):
         os.makedirs(self.playlist_path)

      # declaring a dictionary to hold the playlists
      self.playlists = {}

      # get the name of all the playlists
      print "Reading the name of all the playlists"
      for current_dir, subdirs, files in walk(self.playlist_path):
         # iterate on all the playlists
         for playlist in files:
            # get the name of the playlist
            playlist_name = os.path.splitext(playlist)[0]
            self.playlists[playlist_name] = {}
            # and its full path
            playlist_path = join(current_dir, playlist)
            # create the inner data
            self.playlists[playlist_name]["name"] = playlist_name
            self.playlists[playlist_name]["path"] = playlist_path
            self.playlists[playlist_name]["songs"] = []
            self.playlists[playlist_name]["songs_paths"] = []

         print "Found {0} playlists".format(len(self.playlists))

      return self.playlists


   def populate_playlists(self):
       # repeat for all the paylists
       for playlist in self.playlists:
           playlist_path = self.playlists[playlist]["path"]
           # get the songs
           songs, paths = self.read_pls(playlist_path)

           self.playlists[playlist]["songs"] = songs
           self.playlists[playlist]["songs_paths"] = paths

           print "Playlist {0} has {1} songs".format(playlist, len(self.playlists[playlist]["songs"]))

       return self.playlists


   def save_playlists(self, playlists):
       for playlist in playlists:
           if(playlists[playlist]["modified"]):
               self.write_pls(playlists[playlist])
               print "Saved {0}".format(playlists[playlist]["name"])

       print "Wrote playlists to disk."


   ''' Generic method which determines the correct playlist format
       and parses it accordingly
   '''
   def read_playlist(self, playlist):
      basename = os.path.basename(playlist)

      if basename.endswith(".pls"):
         return self.read_pls(playlist)
      elif basename.endswith(".m3u8"):
         print "Playlist format not supported yet."
         return None, None
      else:
         print "Unknown playlist format."
         return None, None

   '''
   Create a .pls playlist file given a playlist dictionary
   '''
   def write_pls(self, playlist):
      playlist_file = playlist["path"]
      with open("{}.pls".format(name), "w") as playlist:
         # variable to count the songs
         songs=1
         playlist.write("[playlist]\n")
         playlist.write("Title={}\n".format(name))
         for file in os.listdir(base_path):
            if file.endswith(".mp3"):
               playlist.write("File{}=file://{}\n".format(songs, os.path.join(base_path, file)))
               playlist.write("Title{}={}\n".format(songs, os.path.basename(file)))
               songs+=1

         playlist.write("NumberOfEntries={}\n".format(songs-1))
         # write the version of the playlist, 2 is currently valid one
         playlist.write("Version=2")

   '''
   Read a .pls playlist file to get data used to play songs
   '''
   def read_pls(self, fullname):
      songs_titles = []
      songs_paths = []
      lines = []
      with open(fullname, "r") as playlist:
         lines = playlist.readlines()

      for i in range(len(lines)):
         line = lines[i]
         if "File" in line:
            # get the file path
            starting_path = line.split("=")
            song_path = starting_path[1][7:]#.replace("%20", " ")
            songs_paths.append(song_path.strip())
            # get the title
            i+=1
            starting_title = lines[i].split("=")
            songs_titles.append(starting_title[1].strip())
            #print file_path

      return songs_titles, songs_paths


   def create_m3u8(self, base_path, name):
      with open("{}.m3u8".format(name), "w") as playlist:
         playlist.write("#EXTM3U\n")
         for file in os.listdir(base_path):
            if file.endswith(".mp3"):
               playlist.write("#EXTINF:-1,{}\n".format(os.path.basename(file)))
               playlist.write("file://{}\n".format(os.path.join(base_path, file)))
               #playlist.write("file://{}\n".format(os.path.join(base_path, file).replace(" ", "%20").replace("(", "%28").replace(")", "%29")))

# .replace("", "'")

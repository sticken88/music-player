# to walk the filesystem
import os
from os import walk
from os.path import join

class PlaylistManager():

   # basic path
   playlist_dir = join("./", "playlists/")
   # declaring a dictionary to hold the playlists
   playlists = {}

   def get_playlists(self):
      # check if the data is empty or not
      if len(self.playlists):
          return self.playlists
      else:
          # create the playlists folder if missing
          if not os.path.exists(self.playlist_dir):
              os.makedirs(self.playlist_dir)

          # get the name of all the playlists
          print "Reading the name of all the playlists"
          for current_dir, subdirs, files in walk(self.playlist_dir):
             # iterate on all the playlists
             for playlist in files:
                 # get the name of the playlist
                 playlist_name = os.path.splitext(playlist)[0]
                 # and its full path
                 playlist_path = join(current_dir, playlist)
                 self.create_playlist_entry(playlist_name, playlist_path)

             print "Found {0} playlists".format(len(self.playlists))

      return self.playlists


   def create_playlist(self, playlist_name):
       playlist_path = join(self.playlist_dir, playlist_name + ".pls")
       self.create_playlist_entry(playlist_name, playlist_path)
       # write an empty playlist structure
       self.write_pls(self.playlists[playlist_name])
       print "Created playlist {0}, saved in {1}".format(playlist_name, playlist_path)
       print "Now there are {0} playlists".format(len(self.playlists))


   def create_playlist_entry(self, playlist_name, playlist_path):
       # create the inner data
       self.playlists[playlist_name] = {}
       self.playlists[playlist_name]["name"] = playlist_name
       self.playlists[playlist_name]["path"] = playlist_path
       self.playlists[playlist_name]["modified"] = 0
       self.playlists[playlist_name]["songs"] = []
       self.playlists[playlist_name]["songs_paths"] = []


   def delete_playlist_entry(self, playlist):
       del self.playlists[playlist]["name"]
       del self.playlists[playlist]["path"]
       del self.playlists[playlist]["modified"]
       # delete the lists
       del self.playlists[playlist]["songs"][:]
       del self.playlists[playlist]["songs_paths"][:]
       del self.playlists[playlist]


   def delete_playlist(self, playlist):
       """Delete a playlist.
       Removes a playlist from the dictionary and
       deletes the corresponding file on disk.
       """
       # remove the file
       os.remove(self.playlists[playlist]["path"])
       # delete the object from the dictionary
       self.delete_playlist_entry(playlist)


   def rename_playlist(self, playlist, new_name):
       """Rename a playlist.
       Receives the playlist that must be renamed
       and the new name.
       """
       # rename the old file to the new one
       new_playlist_path = join(self.playlist_dir, new_name+".pls")
       os.rename(self.playlists[playlist]["path"], new_playlist_path)

       # Rename the name of the playlist inside the .pls file
       with open(new_playlist_path, "r") as pls_file:
           lines = pls_file.readlines()

       lines[1] = "Title=" + new_name + "\n"

       # write back the file
       with open(new_playlist_path, "w") as pls_file:
           pls_file.writelines(lines)

       # create a new entry in the dictionary
       self.create_playlist_entry(new_name, new_playlist_path)
       # cannot copy the old one to the new because it copies the pointer
       self.playlists[new_name]["songs"] = list(self.playlists[playlist]["songs"])
       self.playlists[new_name]["songs_paths"] = list(self.playlists[playlist]["songs_paths"])
       # and finally deletes the old entry
       self.delete_playlist_entry(playlist)


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
               print "Saved '{0}''".format(playlists[playlist]["name"])

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

      with open("{}".format(playlist["path"]), "w") as playlist_file:
         # write the header
         playlist_file.write("[playlist]\n")
         playlist_file.write("Title={}\n".format(playlist["name"]))
         # loop on all the songs
         songs = playlist["songs"]
         paths = playlist["songs_paths"]
         number_of_songs = len(songs)
         for i in range(0, number_of_songs):
             playlist_file.write("File{}=file://{}\n".format(i+1, paths[i]))
             playlist_file.write("Title{}={}\n".format(i+1, songs[i]))

         playlist_file.write("NumberOfEntries={}\n".format(number_of_songs))
         # write the version of the playlist, 2 is the currently valid one
         playlist_file.write("Version=2")

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

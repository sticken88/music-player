import os

class PlaylistManager():

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
   Create a .pls playlist file with name "name" given a path
   '''
   def create_pls(self, base_path, name):
      #base_path = "/home/matteo/Music"
      with open("{}.pls".format(name), "w") as playlist:
         # variable to count the songs
         songs=1 
         playlist.write("[playlist]\n")
         playlist.write("Title={}\n".format(name))
         for file in os.listdir(base_path):
            if file.endswith(".mp3"):
               playlist.write("File{}=file://{}\n".format(songs, os.path.join(base_path, file))) # .replace(" ", "%20")
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
      with open(fullname, "r") as playlist:
         lines = playlist.readlines()

      for i in range(len(lines)):
         line = lines[i]
         if "File" in line:
            # get the file path
            starting_path = line.split("=")
            song_path = starting_path[1][7:]#.replace("%20", " ")
            songs_paths.append(song_path)
            # get the title
            i+=1
            starting_title = lines[i].split("=")
            songs_titles.append(starting_title[1])
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


manager = PlaylistManager()
manager.create_pls("/home/matteo/Music", "nuova_pls")
manager.create_m3u8("/home/matteo/Music", "nuova_pls")
titles, paths = manager.read_playlist("nuova_pls.pls")

#for i in range(len(titles)):
   #print titles[i] + " || " + paths[i]

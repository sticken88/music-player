import os

class PlaylistManager():
   def create_pls(self, base_path, name):
      #base_path = "/home/matteo/Music"
      with open("{}.pls".format(name), "w") as playlist:
         # variable to count the songs
         songs=1 
         playlist.write("[playlist]\n")
         playlist.write("Title={}\n".format(name))
         for file in os.listdir(base_path):
            if file.endswith(".mp3"):
               playlist.write("File{}=file://{}\n".format(songs, os.path.join(base_path, file).replace(" ", "%20").replace("(", "%28").replace(")", "%29")))
               playlist.write("Title{}={}\n".format(songs, os.path.basename(file)))
               songs+=1

         playlist.write("NumberOfEntries={}\n".format(songs-1))
         # write the version of the playlist, 2 is currently valid one
         playlist.write("Version=2")

   def read_pls(self, fullname):
      with open(fullname, "r") as playlist:
         lines = playlist.readlines()

      for i in range(len(lines)):
         line = lines[i]
         if "File" in line:
            i+=1
            title = lines[i]
            print title


   def create_m3u8(self, base_path, name):
      with open("{}.m3u8".format(name), "w") as playlist:
         playlist.write("#EXTM3U\n")
         for file in os.listdir(base_path):
            if file.endswith(".mp3"):
               playlist.write("#EXTINF:-1,{}\n".format(os.path.basename(file)))
               playlist.write("file://{}\n".format(os.path.join(base_path, file).replace(" ", "%20").replace("(", "%28").replace(")", "%29")))

#create_m3u8()
manager = PlaylistManager()
manager.create_pls("/home/matteo/Music", "nuova_pls")
manager.read_pls("RecentlyAdded.pls")

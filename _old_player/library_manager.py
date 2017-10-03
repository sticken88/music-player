import os

class LibraryManager():

   def __init__(self):
   	#declare data structure to store the songs
   	self.library_songs = []
   	self.library_folder = "music_library"
   	self.file_name = "library"
   	#check if the library folder exists, otherwise crete it
   	if not os.path.isdir(self.library_folder):
   		print "'{}' folder doesn't exist, creating it..".format(self.library_folder)
   		#create the music library folder
   		os.makedirs(self.library_folder)
   		print "..'{}' folder created".format(self.library_folder)
   	else:
   		print "'{} folder exists, loading songs..".format(self.library_folder)


   def parse_library(self):
       songs_paths = []
       lines = []

       with open(os.path.join(self.library_folder, self.file_name), "r") as library:
           for line in library:
              songs_paths.append(line)

       return songs_paths
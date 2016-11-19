import os

class LibraryManager():

   def __init__(self):
   	#declare data structure to store the songs
   	self.library_songs = []
   	self.library_folder = "music_library"
   	self.file_name = "library"
   	#check if the library folder exists, otherwise crete it
   	if not os.path.isdir(library_folder):
   		print "'{}' folder doesn't exist, creating it..".format(library_folder)
   		#create the music library folder
   		os.makedirs(library_folder)
   		print "..'{}' folder created".format(library_folder)
   	else:
   		print "'{} folder exists, loading songs..".format(library_folder)


   def parse_library(self):
       library = open(self.file_name, 'a')

l_library = LibraryManager()
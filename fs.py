class PyFile:
   'Base class for all files stored in the file system'
   empCount = 0
   isDir = false
   isOpen = false
   position = 0

   def __init__(self, path, size, isDir):
      self.path = path
      self.size = size
      self.isDir = isDir
      # parse out name based on end of path #
   
   def open(self, read):
     # TODO #
     # read handles the 'r' and 'w' cases for read and write and sets variables internally #

   def close(self):
      # TODO #
      # Check read/write variable to see if able to close #

   def length(self):
      # TODO #

   def seek(self, position):
      self.position = position
      # TODO #

   def read(self, bytes):
      # TODO read amount of bytes from current position and return #

   def write(self, writeBuf):
      # TODO write STRING writeBuf to end of current file data #

   def readLines(self, bytes):
      # Read all lines in file and return as list of strings (DOES NOT CHANGE POSITION) #

   def delete(self):
      # delete file (based on directory boolean, it will handle how it deletes the file internally) #

   def isDir(self):
      return isDir

   def listDir(self):
      # TODO list directorys #

class fs:
   'Base class for whole file system'
   files = {} # dictionary of all files in file system. --KEY=absolute path, --VALUE=File object

   def __init__(self, f, name):
      self.f = f # This is the root file of the file system that is created by default # # TODO #
      self.name = name
      # parse out name based on end of path #
   
   def create(self, filename, nbytes):
      # Call File object create method #
      # TODO handle exceptions for space #
      # all bytes initialized to 0 #

   def mkdir(self, dirname):
      # create new file object and initialize isDir to true #

   def open(self, filename, mode):
      # Handle exceptions for file system suspension and whether file exists or not #
      # TODO #

   def close(self, fd):
      # Takes file descriptor, locates file, and calls close method on file object directly #
      # TODO #

   def length(self, fd):
      # Call length method on file object itself #

   def pos(self, fd):
      # Call pos method on file object itself #

   def seek(self, fd, pos):
      # Call seek method on file object itself #

   def read(self, fd, nbytes):
      # Call read method on file object itself #
      # Handle exceptions for going beyond file size #

   def write(self, fd, writebuf):
      # Call write method on file object itself #

   def readlines(self, fd):
      # Call readlines method on file object itself #

   def delfile(self, filename):
      # Remove file from dictionary (if it exists) and call delete method on file object itself #

   def deldir(self, dirname):
      # Remove file from dictionary (if it exists), update all keys in dictionary with this directory above them, call delete method on file object itself #

   def isdir(self, filename):
      # Call isdir() on file object itself #

   def listdir(self, filename):
      # List all directories from the dictionary data structure #

   def suspend(self):
      # TODO supspend filesystem operations (set a variable) #
      # All file objects in data structure will be serialized and saved to a save file #

   def resume(self):
      # TODO resume filesystem operations (set a variable) #


import os

# Global Variables #
files = {} # dictionary of all files in file system. --KEY=absolute path, --VALUE=File object
f = "" # 

# Methods to call using the python terminal #
# Many of these methods are just wrapper calls to the underlying pyfile objects #

def init(fsname):
    f = fsname
    if os.path.isfile(fsname):
        file = open(fsname, 'w')
        file.seek(0)
        file.truncate()
    else:
        # Just open it
        file = open(fsname, 'w')
        # Initialize the native file in which storage is done
    print "[INFO] FileSystem with name %s has been created." % f

def create(filename, nbytes):
    # Call File object create method #
    # TODO handle exceptions for space #
    # all bytes initialized to 0 #
    files[filename] = pyfile(filename, nbytes, False)
    return files[filename]

def mkdir(dirname):
    directory = pyfile(dirname, 0, True) # initialize a new pyfile object with isdir set to true
    files[dirname] = directory # add the pyfile object to the dictionary global datastructure
    print "[INFO] A new directory with location ~%s, has been created" % dirname
    return directory

def open(filename, mode):
    # Handle exceptions for file system suspension and whether file exists or not #
    # TODO #
    return 0

def close(fd):
    # Takes file descriptor, locates file, and calls close method on file object directly #
    # TODO #
    return 0

def length(fd):
    # Call length method on file object itself #
    return 0

def pos(fd):
    file = files[fd]
    if file != None:
        return file.position
    return -1

def seek(fd, pos):
    # Call seek method on file object itself #
    return 0

def read(fd, nbytes):
    # Call read method on file object itself #
    # Handle exceptions for going beyond file size #
    return 0

def write(fd, writebuf):
    if fd in files:
        files[fd].open()
    else:
        print "Not in directory. Error handling will go here"

def readlines(fd):
    # Call readlines method on file object itself #
    return 0

def delfile(filename):
    if filename in files: # TODO will also need to check that it is not a directory
        files[filename].delete()
        return True
    return False

def deldir(dirname):
    # Remove file from dictionary (if it exists), update all keys in dictionary with this directory above them, call delete method on file object itself #
    return 0

def isdir(filename):
    # Call isdir() on file object itself #
    return 0

# List all directories from the dictionary data structure #
def listdir(filename):
    #TODO in the future this will need to only list directories that are nested within the 'filename'
    for key in files:
        file = d[key]
        if file.isdir:
            print file.path

def suspend():
    # TODO supspend filesystem operations (set a variable) #
    # All file objects in data structure will be serialized and saved to a save file #
    return 0

def resume():
    # TODO resume filesystem operations (set a variable) #
    return 0

# python file class used to store information about each file object #
class pyfile:
    'Base class for all files stored in the file system'
    contents = []
    isdir = False
    isopen = False
    position = 0
    size = 0

    def __init__(self, path, maxsize, isdir):
        self.path = path
        self.maxsize = maxsize
        self.isdir = isdir
        # parse out name based on end of path #
    
    def open(self, read):
      self.isopen = True
      # TODO #
      # read handles the 'r' and 'w' cases for read and write and sets variables internally #

    def close(self):
        # TODO #
        self.isopen = False
        # Check read/write variable to see if able to close #

    def length(self):
        return len(self)

    def seek(self, position):
        self.position = position
        # TODO #

    def read(self, bytes):
        # TODO read amount of bytes from current position and return #
        return 0

    def write(self, writeBuf):
        # Check if file is open
        if self.isopen:
            contents.append(writeBuf)
        else:
            print "Error : File is closed"

    def readLines(self, bytes):
        # Read all lines in file and return as list of strings (DOES NOT CHANGE POSITION) #
        return 0

    def delete(self):
        if self.isdir:
            for key in files:
                file = d[key]
                if file.isdir and file.path in self.path: # TODO this may need to be modified (maybe create an external comparison method)
                    del files[file.path]
        else
            del files[self.path]

    def isdir(self):
        return self.isdir
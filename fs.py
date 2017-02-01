import os

# Global Variables #
files = {} # dictionary of all files in file system. --KEY=absolute path, --VALUE=File object
f = ""

# Methods to call using the python terminal #
# Many of these methods are just wrapper calls to the underlying pyfile objects #

def init(fsname):
    f = fsname
    if os.path.isfile(fsname):
        file = open(fsname, 'w')
        file.seek(0)
        file.truncate()
    else:
        file = open(fsname, 'w')
    print "[INFO] FileSystem with name %s has been created." % f

def create(filename, nbytes):
    # TODO handle exceptions for space #
    files[filename] = pyfile(filename, nbytes, False)
    print '[INFO] Created file %s with %d bytes.' % (filename, nbytes)
    return files[filename]

def mkdir(dirname):
    directory = pyfile(dirname, 0, True) # initialize a new pyfile object with isdir set to true
    files[dirname] = directory # add the pyfile object to the dictionary global datastructure
    print "[INFO] A new directory with location ~%s, has been created" % dirname
    return directory

def open(filename, mode):
    # Handle exceptions for file system suspension and whether file exists or not #
    if filename in files:
        files[filename].open(mode)
    elif filename not in files and mode == 'w':
        # Note: File will be closed upon calling the close method.
        # Figure this out later
        # Default pyfile to 0 bytes and filename as the name
        new_file = pyfile(filename, 0, False)
        new_file.open('w')
    else:
        print 'Error : Reading file which does not exist'

def close(fd):
    try:
        files[fd].close()
    except LookupError:
        print "Error: File not opened"


def length(fd):
    if fd in files:
        print '[INFO] Size of file %s: %d' % (fd, files[fd].length())
    else:
        print 'Error: File not in directory'


def pos(fd):
    file = files[fd]
    if file != None:
        return file.position
    return -1

#def seek(fd, pos):
#    # Call seek method on file object itself #
#    return 0

def read(fd, nbytes):
    if fd in files:
        files[fd].read(nbytes)
    else:
        print 'File not in Directory. Use error handling later?'

def write(fd, writebuf):
    if fd in files:
        # files[fd].open() NEEDS TO BE OPEN FIRST?
        files[fd].write(writebuf)
    else:
        print "Not in directory. Error handling will go here"

#def readlines(fd):
#    # Call readlines method on file object itself #
#    return 0

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
    mode = ''
    position = 0
    size = 0

    def __init__(self, path, maxsize, isdir):
        self.path = path
        self.maxsize = maxsize
        self.isdir = isdir
        # parse out name based on end of path #

    def open(self, mode):
        self.isopen = True
        if mode == 'r':
            self.mode = 'r'
            print '[INFO] Opened file %s in mode \'%s\'' % (self.path, mode)
        elif mode == 'w':
            self.mode = 'w'
            print '[INFO] Opened file %s in mode \'%s\'' % (self.path, mode)
        else:
            print 'Invalid file mode'

      # read handles the 'r' and 'w' cases for read and write and sets variables internally #

    def close(self):
        if self.isopen:
            self.isopen = False
            self.mode   = '' # Resets the mode the file is at
            print '[INFO] Closed file %s' % self.path
        else:
            print '[INFO] %s already closed' % self.path

    def length(self):
        return self.size

    def seek(self, position):
        self.position = position
        # TODO #

    #def read(self, bytes):

    def write(self, writeBuf):
        # Check if file is open
        if self.isopen and self.mode == 'w':
            # Check if there are any new lines in the write buf
            if '\n' in writeBuf:
                splitStr = writeBuf.split('\n')
                splitStr = splitStr[:-1] # Removes last element, which is empty

                # Checks if entire buffer fits. Quite inefficient however,
                bufsize = 0
                for line in splitStr:
                    bufsize += len(line) + 1

                if self.size + bufsize < self.maxsize:
                    print '[INFO] Printing things with new lines'
                    for line in splitStr:
                        self.size += len(line) + 1
                        self.contents.append(line + '\n')
                else:
                    print 'Error. Exceeded Write buffer size (on \\n strings)'
            else: # No new line chracter
                # Check if buffer size is exceeded
                if self.size + len(writeBuf) < self.maxsize:
                    print '[INFO] Writing %s to file %s' % (writeBuf, self.path)
                    self.size += len(writeBuf)
                    self.contents.append(writeBuf)
                else:
                    print 'Error. Exceeded Write buffer size'
        else:
            print "Error : File is closed or not allowed to write to"

    #def readLines(self, bytes):
    #    # Read all lines in file and return as list of strings (DOES NOT CHANGE POSITION) #
    #    return 0

    def delete(self):
        if self.isdir:
            for key in files:
                file = d[key]
                if file.isdir and file.path in self.path: # TODO this may need to be modified (maybe create an external comparison method)
                    del files[file.path]
        else:
            del files[self.path]

    def isdir(self):
        return self.isdir

    def isdir(self):
        return self.isdir

    #def listdir(self):
    #    # TODO list directorys #
    #    return 0

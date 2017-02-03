import os

# Global Variables #
# Directories stored in files as a hash.
#   key = absolute path
#   value = file object
files = {}
f = ""

def init(fsname):
    """ init(fsname)
        Initializes the filesystem. Destroys the contents of the
        file if a file already exists. """
    f = fsname
    if os.path.isfile(f):
        file = open(fsname, 'w')
        file.seek(0)
        file.truncate()
        file.close()
    print "[INFO] FileSystem with name %s has been created." % f


def create(filename, nbytes):
    """ create(filename, nbytes)
        Creates a file with the name 'filenames' and places the file
        in a hash table. The absolute path will be they key. """
    # Still need to implament exception for when allocation fails
    # and figure out how to initialize bytes to NULLs
    try:
        files[filename] = pyfile(filename, nbytes, False)
        print '[INFO] Created file %s with %d bytes.' % (filename, nbytes)
    except:
        print 'Error allocating number of bytes'
    return files[filename]


def mkdir(dirname):
    """ mkdir(dirname)
        Creates directory and stores the key in the files hash. """
    # Need to implament a way to change directories with absolut path
    directory = pyfile(dirname, 0, True) # initialize a new pyfile object with isdir set to true
    files[dirname] = directory # add the pyfile object to the dictionary global datastructure
    print "[INFO] A new directory with location ~%s, has been created" % dirname


def open(filename, mode):
    """ open(filename, mode)
        Opens a file in the filesystem. If the file is not in the
        filesyste, create a file and continue on."""
    # Handle exceptions for file system suspension
    # and whether file exists or not
    if filename in files:
        # Open file if in filesystem
        files[filename].open(mode)
    elif filename not in files and mode == 'w':
        # If not, create file in filesystem
        new_file = pyfile(filename, 0, False)
        new_file.open('w')
    else:
        # Exceptions go here
        print 'Error : something went wrong in open()'


def close(fd):
    try:
        # Try closing file
        files[fd].close()
    except LookupError:
        print "Error: File not opened"


def length(fd):
    try:
        print '[INFO] Size of file %s: %d' % (fd, files[fd].length())
    except LookupError:
        print 'Error: File not in directory'

def pos(fd):
    try:
        print '%s position: %d' % (fd, files[fd].position)
    except LookupError:
        print 'Error: File not in directory'

def seek(fd, pos):
    if fd in files:
        files[fs].seek(pos)
    else:
        print 'Error : File not in directory'

def read(fd, nbytes):
    try:
        readString = files[fd].read(nbytes)
        #assuming we have to print out readString
        print readString
    except LookupError:
        print 'Error: File not in directory'

def write(fd, writebuf):
    try:
        files[fd].write(writebuf)
    except LookupError:
        print 'Error: File not in directory'

def readlines(fd):
    try:
        file_contents = files[fd].readLines()
        # Later, we will put in a way to return a list
        # but for now, print to screen
        for lines in file_contents:
            print '%s' % lines
    except LookupError:
        print 'Error: File not in directory'

def delfile(filename):
    # Also needs to check if not a directory
    try:
        files[filename].delete()
        return True
    except:
        return False

def deldir(dirname):
    # Remove file from dictionary (if it exists), update all keys in
    # dictionary with this directory above them, call delete
    # method on file object itself #
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
    pickle.dump(files, open("data.p", "wb"), pickle.HIGHEST_PROTOCOL)


def resume():
    # TODO resume filesystem operations (set a variable) #
    return 0

# python file class used to store information about each file object #
class pyfile:
    'Base class for all files stored in the file system'
    isdir = False
    isopen = False
    mode = ''
    size = 0

    def __init__(self, path, maxsize, isdir):
        self.path = path
        self.maxsize = maxsize
        self.isdir = isdir
        self.contents = []
        self.position = 0
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

    def seek(self, pos):
        if pos < 0:
            print 'Error : Negative position'
        elif pos > self.maxsize:
            print 'Error : Exceeded size'
        else:
            self.position = pos
            print '[INFO] Placing position to %d.' % pos


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

    def read(self, nbytes):
        #Check if file is open and read mode
        #how to deal with bytes
        readString = ' '
        if self.isopen and self.mode == 'r':
            if nbytes > self.maxsize:
                print "Error: Exceeded file size "
            if nbytes > self.size:
                print "Error: Exceeded current file size "
            else:
                for i in range(nbytes):
                    readString+=str(self.contents[i])
                    #position is affected by read?
                    # self.pos+=i
                return readString


    def readLines(self):
         strList = []
         for lines in self.contents:
             strList.append(lines)
         return strList

    def delete(self):
        if self.isdir:
            for key in files:
                file = d[key]
                if file.isdir and file.path in self.path:
                    # TODO this may need to be modified (maybe create an external comparison method)
                    del files[file.path]
        else:
            del files[self.path]

    def isdir(self):
        return self.isdir

    def isdir(self):
        return self.isdir

    #def listdir(self):
    #    # TODO list directorys #

import os

# Globals
class glb:
    files = {} # --Key : absolute file path, item : pyfile
    curr_dir = '/' # Tracking variable for current directory
    fsname = None

###########################################################################
### HELPER FUNCTIONS
###########################################################################
def generate_filepath(filename):
    """ generate_filepath(filename)
        Generates a full filepath for a directory / file. """
    if str(glb.curr_dir) == '/': # Special case, root directory
        dict_filename = glb.curr_dir + filename
    else:
        dict_filename = glb.curr_dir + '/' + filename
    return dict_filename


###########################################################################
### fs module functions
###########################################################################
def init(fsname):
    glb.fsname = fsname
    if os.path.isfile(fsname):
        file = open(fsname, 'w')
        file.seek(0)
        file.truncate()
        file.close()
    # Initalize a root directory
    glb.files['/'] = pyfile('/', 0, True)
    print "--[INFO] FileSystem with name %s has been created." % fsname


def create(filename, nbytes):
    dict_filepath = generate_filepath(filename) # Name of filepath
    glb.files[glb.curr_dir].add_file(filename)
    glb.files[dict_filepath] = pyfile(filename, nbytes, False)
    print '--[INFO] Created file %s with %d bytes created in %s.' \
            % (filename, nbytes, glb.curr_dir)


def mkdir(dirname):
    dict_dirpath = generate_filepath(dirname) # Name of directory path
    glb.files[glb.curr_dir].add_file(dirname)
    glb.files[dict_dirpath] = pyfile(dirname, 0, True)
    print "--[INFO] A new directory %s with location %s, has been created" \
            % (dirname, glb.curr_dir)


def open(filename, mode):
    if glb.files[glb.curr_dir].in_curr_dir(filename):
        dict_filepath = generate_filepath(filename)
        glb.files[dict_filepath].open(mode)
        print '--[INFO] Opened file %s located in directory %s' \
                % (filename, glb.curr_dir)
    else:
        print '--[ERROR] File not in directory'

    #elif filename not in glb.files and mode == 'w':
    #    # If not, create file in filesystem
    #    # Write will handle adding file to hash
    #    new_file = pyfile(filename, 0, False)
    #    new_file.open('w')
    #    print '[INFO] Opening file which is not in directory'
    #else:
    #    # Exceptions go here
    #    print 'Error : something went wrong in open()'


def write(fd, writebuf):
    if glb.files[glb.curr_dir].in_curr_dir(fd):
        dict_filepath = generate_filepath(fd)
        glb.files[dict_filepath].write(writebuf)
        print '--[INFO] Written to file %s' % fd
    #try:
    #    #fd = glb.curr_dir + fd
    #    glb.files[fd].write(writebuf)
    #except LookupError:
    #    print 'Error: File not in directory'


def close(fd):
    if glb.files[glb.curr_dir].in_curr_dir(fd):
        dict_filepath = generate_filepath(fd)
        glb.files[dict_filepath].close()
        print '--[INFO] Closed file %s located in director %s' \
                % (fd, glb.curr_dir)

###################################################
def length(fd):
    try:
        print '[INFO] Size of file %s: %d' % (fd, glb.files[fd].length())
    except LookupError:
        print 'Error: File not in directory'


def pos(fd):
    try:
        print '%s position: %d' % (fd, glb.files[fd].position)
    except LookupError:
        print 'Error: File not in directory'


def seek(fd, pos):
    if fd in glb.files:
        glb.files[fs].seek(pos)
    else:
        print 'Error : File not in directory'


def read(fd, nbytes):
    try:
        readString = glb.files[fd].read(nbytes)
        #assuming we have to print out readString
        print readString
    except LookupError:
        print 'Error: File not in directory'


def readlines(fd):
    try:
        file_contents = glb.files[fd].readLines()
        # Later, we will put in a way to return a list
        # but for now, print to screen
        for lines in file_contents:
            print '%s' % lines
    except LookupError:
        print 'Error: File not in directory'


def delfile(filename):
    # Also needs to check if not a directory
    try:
        glb.files[filename].delete()
        return True
    except:
        return False


def chdir(dirname):
    # Special case, go back a directory
    if str(dirname) == '..' or str(dirname) == '../':
        dir_list = glb.curr_dir.split('/')
        glb.curr_dir = '/'
        # Set directory path
        for dir in dir_list[1:-1]:
            glb.curr_dir = glb.curr_dir + dir
    # Special case, go to same directory
    elif str(dirname) == '.':
        return # This does nothing, just here to not trigger else statement
    # Changes to different directory, if in the file hash
    elif glb.files[glb.curr_dir].in_curr_dir(dirname):
        if glb.curr_dir == '/':
            glb.curr_dir = glb.curr_dir + dirname
        else:
            glb.curr_dir = glb.curr_dir + '/' + dirname
    else:
        print 'Error: Directory not found'


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
    for key in glb.files:
        file = d[key]
        if file.isdir:
            print file.path


def suspend():
    pickle.dump(files, open("data.p", "wb"), pickle.HIGHEST_PROTOCOL)


def resume():
    # TODO resume filesystem operations (set a variable) #
    return 0


###################
def print_keys():
    for key in glb.files.keys():
        print key



# python file class used to store information about each file object #
class pyfile:
    'Base class for all files stored in the file system'

    def __init__(self, path, maxsize, isdir):
        self.path = path
        self.isdir = isdir
        self.contents = []
        self.size = 0
        # If not isdir, than is file, so initialze file variables.
        if not isdir:
            self.maxsize = maxsize
            self.position = 0
            self.isopen = False
            self.mode = 'closed'
        # parse out name based on end of path #

    ###########################################################################
    ### FILE OPERATIONS
    ###########################################################################
    def open(self, mode):
        self.isopen = True
        if mode == 'r':
            self.mode = 'r'
            print '--[INFO] Opened file %s in mode \'%s\'' % (self.path, mode)
        elif mode == 'w':
            self.mode = 'w'
            print '--[INFO] Opened file %s in mode \'%s\'' % (self.path, mode)
        else:
            print '--[ERROR] Invalid file mode'


    def close(self):
        if self.isopen:
            self.isopen = False
            self.mode   = 'closed' # Resets the mode the file is at
            print '--[INFO] Closed file %s' % self.path
        else:
            print '--[ERROR] %s already closed' % self.path


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
                    print '--[INFO] Printing things with new lines'
                    for line in splitStr:
                        self.size += len(line) + 1
                        self.contents.append(line + '\n')
                else:
                    print 'Error. Exceeded Write buffer size (on \\n strings)'
            else: # No new line chracter
                # Check if buffer size is exceeded
                if self.size + len(writeBuf) < self.maxsize:
                    print '--[INFO] Writing %s to file %s' \
                            % (writeBuf, self.path)
                    self.size += len(writeBuf)
                    self.contents.append(writeBuf)
                else:
                    print '--[ERROR] Exceeded Write buffer size'
        else:
            print "--[ERROR] File is closed or not allowed to write to"


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


    ###########################################################################
    ### DIRECTORY OPERATIONS
    ###########################################################################
    def add_file(self, filename):
        if self.isdir and filename not in self.contents:
            self.contents.append(filename)
        else:
            print "Error Making Directory"


    def in_curr_dir(self, filename):
        if self.isdir and filename in self.contents:
            return True
        else:
            return False


    def isdir(self):
        return self.isdir


    def isdir(self):
        return self.isdir


    #def listdir(self):
    #    # TODO list directorys #

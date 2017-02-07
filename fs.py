import os
import io
import pickle

# Globals
class glb:
    fsname    = None
    curr_dir  = '/' # Tracking variable for current directory
    files     = {} # --Key : absolute file path, item : pyfile
    unwritten = {} # Hash for files not in directory, but opened with 'w'
    resume    = 1 #variable used to keep track of process in resume/suspend



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


def check_status():
    if glb.resume == 0:
        raise ValueError( "Process suspended cannot execute" )


###########################################################################
### fs module functions
###########################################################################
def init(fsname):
    glb.fsname = fsname

    dataFileName = '%s.fssave' % fsname
    # print 'File that will possibly be loaded is named %s' % dataFileName
    # if os.path.isfile(dataFileName):
    # 	with open(dataFileName, 'rb') as handle:
    # 		files = pickle.load(handle)

    if os.path.isfile(fsname):
        file = open(fsname, 'w')
        file.seek(0)
        file.truncate()
        file.close()
    # Initalize a root directory
    glb.files['/'] = pyfile('/', 0, True)
    print "--[INFO] FileSystem with name %s has been created." % fsname


def create(filename, nbytes):
    try:

        check_status()
        dict_filepath = generate_filepath(filename) # Name of filepath
        glb.files[glb.curr_dir].add_file(filename)
        glb.files[dict_filepath] = pyfile(filename, nbytes, False)
        print '--[INFO] Created file %s with %d bytes created in %s.' \
                % (filename, nbytes, glb.curr_dir)
    except ValueError:
        print '--[ERROR] Process suspended cannot execute'
    except:
        print '[ERROR] File note created, failure to allocate space'


def mkdir(dirname):
    try:
        check_status()
        dict_dirpath = generate_filepath(dirname) # Name of directory path
        glb.files[glb.curr_dir].add_file(dirname)
        glb.files[dict_dirpath] = pyfile(dirname, 0, True)
        print "--[INFO] A new directory %s with location %s has been created" \
                % (dirname, glb.curr_dir)
    except ValueError:
        print '--[ERROR] Process suspended cannot execute'
    except:
        print '[ERROR] Failed to make directory'


def chdir(dirname):
    try:
        check_status()
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
        elif glb.files[glb.curr_dir].in_dir(dirname):
            glb.curr_dir = generate_filepath(dirname)
    except:
        print 'Error: Directory not found'


def open(filename, mode):
    try:
        check_status()
        if glb.files[glb.curr_dir].in_dir(filename):
            # File is in directory
            dict_filepath = generate_filepath(filename)
            glb.files[dict_filepath].open(mode)
            print '--[INFO] Opened file %s located in directory %s' \
                    % (filename, glb.curr_dir)
        elif not glb.files[glb.curr_dir].in_dir(filename) and str(mode) == 'w':
            # File is not in directory, but write mode, so creates file
            # Don't add into hash until fs.close() is called
            dict_filepath = generate_filepath(filename)
            glb.files[glb.curr_dir].contents.append(filename) # Add to file contents
            # Add unwritten files to a seperate hash
            glb.unwritten[dict_filepath] = pyfile(filename, 1000, False)
            glb.unwritten[dict_filepath].open('w')
            print '--[INFO] Opening file which is not in directory'
            return
    except ValueError:
        print '--[ERROR] Process suspended cannot execute'
    except:
        print '--[ERROR] File not in directory'


def write(fd, writebuf):
    try:
        check_status()
        dict_filepath = generate_filepath(fd)
        if dict_filepath in glb.files:
            glb.files[dict_filepath].write(writebuf)
            print '--[INFO] Written to file %s (file exists in filesystem)' % fd
        else:
            glb.unwritten[dict_filepath].write(writebuf)
            print '--[INFO] Written to file %s (file not in filesystem)' % fd

    except ValueError:
        print '--[ERROR] Process suspended cannot execute'
    except:
        print '--[ERROR] File not in directory'



def close(fd):
    try:
        check_status()
        dict_filepath = generate_filepath(fd)
        if dict_filepath in glb.files:
            glb.files[dict_filepath].close()
            print '--[INFO] Closed file %s located in director %s' \
                    % (fd, glb.curr_dir)
        else: # Unwritten file
            glb.files[dict_filepath] = glb.unwritten[dict_filepath]
            glb.unwritten.pop(dict_filepath)
    except ValueError:
        print '--[ERROR] Process suspended cannot execute'


    except:
        print '--[ERROR] File not in directory'



def close(fd):
    try:
        dict_filepath = generate_filepath(fd)
        if dict_filepath in glb.files:
            glb.files[dict_filepath].close()
            print '--[INFO] Closed file %s located in director %s' \
                    % (fd, glb.curr_dir)
        else: # Unwritten file
            glb.files[dict_filepath] = glb.unwritten[dict_filepath]
            glb.unwritten.pop(dict_filepath)
    except:
        print '--[ERROR] File not in directory'



def read(fd, nbytes):
    try:
        dict_filepath = generate_filepath(fd)
        glb.files[dict_filepath].read(nbytes)

        check_status()
        dict_filepath = generate_filepath(fd)
        glb.files[dict_filepath].read(nbytes)
    except ValueError:
        print '--[ERROR] Process suspended cannot execute'
    except:
        print '--[ERROR] Issue reading from file'


def readlines(fd):
    try:
        check_status()
        dict_filepath = generate_filepath(fd)
        glb.files[dict_filepath].readlines()
    except ValueError:
        print '--[ERROR] Process suspended cannot execute'
    except:
        print '--[ERROR] File not in directory'


def length(fd):
    try:
        check_status()
        dict_filepath = generate_filepath(fd)
        length = glb.files[dict_filepath].length()
        print 'Length of %s : %d' % (fd, length)
    except ValueError:
        print '--[ERROR] Process suspended cannot execute'
    except:
        print '--[ERROR] File not in directory'



def pos(fd):
    try:
        check_status()
        dict_filepath = generate_filepath(fd)
        pos = glb.files[dict_filepath].pos()
    except ValueError:
        print '--[ERROR] Process suspended cannot execute'
    except:
        print '--[ERROR] File not in directory'



def seek(fd, pos):
    try:
        check_status()
        dict_filepath = generate_filepath(fd)
        glb.files[dict_filepath].seek(pos)
    except ValueError:
        print '--[ERROR] Process suspended cannot execute'
    except:
        print '--[ERROR] File not in directory'


def delfile(filename):
    try:
        check_status()
        dict_filepath = generate_filepath(filename)
        glb.files[glb.curr_dir].del_indir(filename)
        glb.files.pop(dict_filepath)
        print '--[INFO] Deleting file %s' % filename
    except ValueError:
        print '--[ERROR] Process suspended cannot execute'
    except:
        print '--[ERROR] File not in directory'


def deldir(dirname):
    try:
        check_status()
        path = generate_filepath(dirname)
        if path in glb.files:
            # Couldn't figure out how to manually remove keys from pyfile for
            # directories without breaking everything
            if glb.files[path].is_empty():
                glb.files.pop(path)
                return

            chdir(dirname)
            for f in glb.files[glb.curr_dir].contents:
                path = generate_filepath(f)
                if glb.files[path].is_dir():
                    # if not directory, recursion to delete every file in directory
                    deldir(f) # Recursion into directory
                else:
                    # if regular file
                    glb.files.pop(path) # Pop regular file in directory
            chdir('..')
            path = generate_filepath(dirname)
            glb.files.pop(path)
    except ValueError:
        print '--[ERROR] Process suspended cannot execute'
    except:
        print '--[ERROR] File not in directory'


def isdir(filename):
    try:
        check_status()
        if str(filename) == '.' or str(filename) == './':
            print '%s is a directory' % filename
        elif str(filename) == '..' or str(filename) == '../':
            print '%s is a directory' % filename
        else:
            dict_filepath = generate_filepath(filename)
            if glb.files[dict_filepath].is_dir():
                print '%s is a directory' % filename
            else:
                print '%s is not a directory' % filename
    except ValueError:
        print '--[ERROR] Process suspended cannot execute'
    except:
        print '--[ERROR] File not in directory'


def listdir(filename):
    try:
        check_status()
        if str(filename) == '.' or str(filename) == './':
            for f in glb.files[glb.curr_dir].contents:
                inner_path = generate_filepath(f)
                # Remove files in pyfile.contents if its not in key
                # This is a sideeffect of getting fs.deldir() working
                if inner_path not in glb.files:
                    glb.files[glb.curr_dir].contents.remove(f)
            print glb.files[glb.curr_dir].contents
            return
        path = generate_filepath(filename)
        chdir(filename)
        for f in glb.files[path].contents:
            inner_path = generate_filepath(f)
            if inner_path not in glb.files:
                glb.files[path].contents.remove(f)
        print glb.files[path].contents
        chdir('..')
    except:
        print '--[ERROR] File not in directory'


def suspend():
    # check to see if any file is open for writing---can't suspend
    for fd in glb.files:
        # print fd
        if glb.files[fd].isdir == False:
            if glb.files[fd].isopen == True and glb.files[fd].mode == 'w':
                print '--[ERROR] cannot suspend there is a file open for writing'
                return
    print '--[INFO] Suspending filesystem'
    glb.resume = 0 # suspending all process
    dataFileName = '%s.fssave' % glb.fsname
    print 'File that is saving will be named %s' % dataFileName
    #create File I/O object
    fo = io.FileIO(dataFileName, "wb")
    pickle.dump(glb.files, fo, protocol=pickle.HIGHEST_PROTOCOL)
    fo.close()

def resume(filename):
    print '--[INFO] Resuming filesystem '+filename
    glb.resume = 1
    #dataFileName = '%s.fssave' % glb.fsname
    fo = io.FileIO(filename, "rb")
    #load saved file into files
    glb.files = pickle.load(fo)
    return


############################################
# USED FOR CHECKING FILESYSTEM. DELETE LATER
############################################
def print_keys():
    for key in glb.files.keys():
        print key



###########################################################################
### PYFILE class
###########################################################################
class pyfile:
    """Base class for all files stored in the file system"""
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


    def length(self):
        return self.size


    def seek(self, pos):
        if self.isdir:
            print '[ERROR] Seeking position in a directory'
        else:
            if pos < 0:
                print 'Error : Negative position'
            elif pos > self.maxsize:
                print 'Error : Exceeded size'
            else:
                self.position = pos
                print '--[INFO] Placing position to %d in file %s.' % \
                        (pos, self.path)


    def write(self, writeBuf):
        # Check if file is open
        if self.isopen and self.mode == 'w':
            # Check if there are any new lines in the write buf
            if '\n' in writeBuf:
                splitStr = writeBuf.split('\n')

                # Checks if entire buffer fits. Quite inefficient however,
                bufsize = 0
                for line in splitStr:
                    bufsize += len(line) + 1 # EOF is a byte 0xa

                if self.size + bufsize < self.maxsize:
                    print '--[INFO] [WRITTING] Printing Multiple lines to file'
                    for line in splitStr:
                        self.size += len(line) + 1
                        self.contents.append(line)
                else:
                    print 'Error. Exceeded Write buffer size (on \\n strings)'
            else: # No new line chracter
                # Check if buffer size is exceeded
                if self.size + len(writeBuf) < self.maxsize:
                    self.size += len(writeBuf) + 1 # +1 for EOF byte
                    self.contents.append(writeBuf)
                    print '--[INFO] [WRITTING] Writing %s to file %s' \
                            % (writeBuf, self.path)
                else:
                    print '--[ERROR] [WRITTING] Exceeded Write buffer size'
        else:
            print "--[ERROR] [WRITTING] File is closed or not allowed to write to"


    def read(self, nbytes):
        if self.isopen and self.mode == 'r':
            if nbytes > self.maxsize:
                print "--[ERROR] Exceeded file size "
            elif nbytes > self.size:
                print "--[ERROR] Exceeded current file size "
            else:

                if len(self.contents) == 1: # Special case, 1 line
                    f_str = ''.join(self.contents) # Turn contents into string
                    start = self.position
                    end   = self.position + nbytes
                    self.position = end # Update position after reading
                    print f_str[start : end]
                else:
                    # Fuck my life
                    idx = 0
                    seek_bytes = 0
                    f_str = ''.join(self.contents[idx])

                    # Seek to position
                    while seek_bytes + len(f_str) + 1 < self.position:
                        seek_bytes = seek_bytes + len(f_str) + 1
                        idx += 1
                        f_str = ''.join(self.contents[idx])

                    # Find exact starting position to read
                    remain = self.position - seek_bytes
                    read_bytes = 0

                    # Print out remaing char of line
                    if len(f_str[remain:]) + 1 >= nbytes:
                        print f_str[remain: remain + nbytes]
                        return
                    else:
                        read_bytes += len(f_str[remain:]) + 1
                        idx += 1
                        print f_str[remain:]

                    # Print all the bytes
                    while read_bytes < nbytes:
                        f_str = ''.join(self.contents[idx])

                        if read_bytes + len(f_str) + 1 > nbytes:
                            print f_str[: nbytes - read_bytes]
                            break
                        else:
                            read_bytes = read_bytes + len(f_str) + 1
                            idx += 1
                            print f_str
        else:
            print '--[ERROR] File is not opened to read'


    def readlines(self):
        if self.isopen and self.mode == 'r':
            str_list = []
            for lines in self.contents:
                line_str = ''.join(lines)
                print line_str
        else:
            print '--[ERROR] File is not opened to read'


    def pos(self):
        if self.isdir:
            print '--[ERROR] Attempting to find position of director'
        else:
            return self.position


    ###########################################################################
    ### DIRECTORY OPERATIONS
    ###########################################################################
    def add_file(self, filename):
        if self.isdir and filename not in self.contents:
            self.size += 1
            self.contents.append(filename)
        else:
            print "Error Making Directory"


    def pos(self):
        if self.isdir:
            print '--[ERROR] Attempting to find position of director'
        else:
            return self.position


    def in_dir(self, filename):
        if self.isdir and filename in self.contents:
            return True
        else:
            return False


    def del_indir(self, filename):
        self.contents.remove(filename)


    def is_dir(self):
        return self.isdir


    def is_empty(self):
        return len(self.contents) == 0

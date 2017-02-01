import fs

def main():
    fs.init('abc')

    # Test file creation and track files
    fs.create('file1.txt', 100)
    fs.create('tmp.dat', 3)
    fs.create('other.c', 2)
    fs.create('d', 10)
    fs.create('ex', 10)

    print '\nCurrent filesystem: %s'
    for files in fs.files.keys():
        print "File : %s" % files

    # Test Opening files
    print '\nTesting opening files'
    fs.open('file1.txt', 'w')
    fs.open('tmp.dat', 'r')
    fs.open('tmp.dat', 'w')
    fs.open('other.c', 'w')
    fs.open('d', 'adsf')

    # Test writing to file
    print '\nTesting writing to files'
    fs.write('file1.txt', 'Something goes in here.')
    fs.write('tmp.dat', 'a\nb\nc\n')
    fs.write('tmp.dat', 'a\n')
    fs.write('other.c', 'THIS_IS_MORE_THAN_2_BYTES')
    fs.write('d', 'fasd')

    # Test close file
    print '\nTesting closing files'
    fs.close('file1.txt')
    fs.write('file1.txt', 'Something goes in here.')
    fs.close('asdf')
    fs.close('ex')

    # Test length of file
    print '\nTesting length of file'
    fs.length('tmp.dat')

if __name__ == '__main__':
    main()

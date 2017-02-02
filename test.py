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
    fs.write('file1.txt', 'Something goes in here.') # Should write
    fs.write('tmp.dat', 'a\nb\nc\n') # Shouldn't write
    fs.write('tmp.dat', 'a\n') # Should write
    fs.write('other.c', 'THIS_IS_MORE_THAN_2_BYTES') # shouldn't write
    fs.write('d', 'fasd') # Should'nt write

    # Test close file
    print '\nTesting closing files'
    fs.close('file1.txt')
    fs.write('file1.txt', 'Something goes in here.')
    fs.close('asdf')
    fs.close('ex')

    # Test length of file
    print '\nTesting length of file'
    fs.length('tmp.dat')

    # Test reading entire file
    print '\nTesting readlines()'
    fs.readlines('file1.txt')
    fs.readlines('tmp.dat')

if __name__ == '__main__':
    main()

import fs

def main():
    fs.init('abc')

    # Test file creation and track files
    fs.create('file1.txt', 100)
    fs.create('tmp.dat', 200)
    fs.create('d', 10)

    print '\nCurrent filesystem: %s'
    for files in fs.files.keys():
        print "File : %s" % files

    # Test Opening files
    print '\nTesting opening files'
    fs.open('file1.txt', 'w')
    fs.open('tmp.dat', 'r')
    fs.open('tmp.dat', 'w')
    fs.open('d', 'adsf')

    # Test writing to file
    print '\nTesting writing to files'
    fs.write('file1.txt', 'Something goes in here.')
    fs.write('tmp.dat', 'a\nb\nc\n')
    fs.write('d', 'fasd')

if __name__ == '__main__':
    main()

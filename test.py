#! /usr/bin/env python

import fs

def main():
    fs.init('myfs')

    # Create a basic directory tree
    print '\nCreating filesystem for testing'
    fs.mkdir('a')
    fs.mkdir('b')
    fs.create('file.txt', 100)
    fs.chdir('a')
    fs.mkdir('c')
    fs.chdir('c')
    fs.create('file_in_c', 1000)
    fs.chdir('../')
    fs.chdir('..')
    fs.chdir('b')
    fs.create('file_in_b', 2)
    fs.chdir('..') # Back to root

    # Print out current tree
    print '\nCurrent Directory Structure'
    fs.print_keys()
    print

    # Test open, write, and close
    print 'Testing Writing to /file.txt'
    fs.open('file.txt', 'w')
    fs.write('file.txt', 'Writing some random stuff')
    fs.close('file.txt')
    print

    # Test print multiple lines
    print 'Changing Directories'
    fs.chdir('a')
    fs.chdir('c')
    print 'Testing writing multiple lines to file'
    fs.open('file_in_c', 'w')
    fs.write('file_in_c', 'Writing\nMultiple\nLines')
    fs.close('file_in_c')
    fs.open('file_in_c', 'r')
    fs.read('file_in_c', 15)
    print

    # Test opneing file not in directory and read
    print 'Changing back to root'
    fs.chdir('../')
    fs.chdir('..')
    print 'Testing opening file not in directory and reading'
    fs.open('not_in_dir', 'w')
    fs.write('not_in_dir', 'Things')
    fs.close('not_in_dir')
    fs.open('not_in_dir', 'r')
    fs.read('not_in_dir', 3)
    fs.read('not_in_dir', 1)
    fs.close('not_in_dir')
    print

    fs.print_keys()

if __name__ == '__main__':
    main()

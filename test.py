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

    # Print out current tree
    print '\nCurrent Directory Structure'
    fs.print_keys()
    print '\n'

if __name__ == '__main__':
    main()

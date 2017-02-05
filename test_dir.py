#! /usr/bin/env python

import fs

def main():
    fs.init('fs')
    fs.mkdir('a')
    fs.mkdir('b')
    fs.mkdir('c')
    fs.chdir('c')
    fs.create('c1', 10)
    fs.create('c2', 10)
    fs.chdir('../')
    fs.chdir('b')
    fs.mkdir('b1')
    fs.mkdir('b2')
    fs.create('b3', 10)
    fs.chdir('b1')
    fs.mkdir('b11')
    fs.chdir('..')
    fs.chdir('..')

    fs.print_keys()
    print

    print 'After Deleting /b'
    fs.deldir('b')
    fs.print_keys()
    print


    print 'After Deleting /c'
    fs.deldir('c')
    fs.print_keys()
    print

    print 'After Deleting /a'
    fs.deldir('a')
    fs.print_keys()
    print

if __name__ == '__main__':
    main()

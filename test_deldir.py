#! /usr/bin/env python

import fs

def main():
    fs.init('fs')
    fs.mkdir('a')
    fs.chdir('a')
    fs.mkdir('b')
    fs.chdir('b')
    fs.mkdir('c')
    fs.create('file_b', 1)
    fs.chdir('..')
    fs.create('file_a', 1)
    fs.chdir('..')

    print
    fs.deldir('a')
    fs.print_keys()



if __name__ == '__main__':
    main()

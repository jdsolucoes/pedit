#!/usr/bin/env python
from __future__ import print_function

import sys
import readline

import os


try:
    readline.read_init_file(os.path.join(os.path.expanduser('~'), 'pedit.rc'))
except IOError:
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set editing-mode emacs')

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        print("git config --global core.editor {}".format(sys.argv[0]))
        sys.exit(1)

    print('Enter commit message bellow. Terminate with Ctrl + D.')
    with open(filename, 'w') as file_obj:
        try:
            lines = sys.stdin.readlines()
            message = '\n'.join(lines)
        except KeyboardInterrupt:
            print("Canceled!")
            sys.exit(1)
        file_obj.write(message)

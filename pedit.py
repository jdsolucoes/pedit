#!/usr/bin/env python
from __future__ import print_function

import sys
import readline

import os

try:
    get_input = raw_input
except NameError:
    # Py3k
    get_input = input

try:
    readline.read_init_file(os.path.join(os.path.expanduser('~'), 'pedit.rc'))
except IOError:
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set editing-mode emacs')

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        assert os.path.exists(filename)
    except (IndexError, AssertionError):
        print("git config --global core.editor {}".format(sys.argv[0]))
        sys.exit(1)

    print("Enter commit message bellow; enter '--' alone on the line to stop")
    with open(filename, 'r+') as file_obj:
        first_line = file_obj.readlines()[0].rstrip()
        file_obj.seek(0)
        if first_line and 'Merge' in first_line:
            print('Press Ctrl + D to keep message: "{}"'.format(first_line))
        lines = []
        while True:
            try:
                line = get_input(':')
            except EOFError:
                print('<eof>')
                break
            except KeyboardInterrupt:
                print("Canceled!")
                sys.exit(1)
            if line == '--':
                break
            lines.append(line)
        message = '\n'.join(lines)
        if not message and first_line:
            message = first_line
        file_obj.write(message)
        file_obj.truncate()

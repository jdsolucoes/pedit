#!/usr/bin/env python
import sys

if __name__ == '__main__':
    with open(sys.argv[1], 'w') as file_obj:
        message = raw_input('Enter commit message: ')
        file_obj.write(message)

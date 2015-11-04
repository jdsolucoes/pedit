#!/usr/bin/env python
import sys

if __name__ == '__main__':
    with open(sys.argv[1], 'w') as file_obj:
        try:
            message = raw_input('Enter commit message: ')
        except KeyboardInterrupt:
            sys.exit(1)
        file_obj.write(message)

#!/usr/bin/env python
import sys

message = raw_input('Enter commit message: ')
message_file_path = sys.argv[1]
message_file = open(message_file_path, 'w')
message_file.write(message)
message_file.close()

#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals

import os
import subprocess
import sys
from prompt_toolkit import prompt

def get_git_info():
    output = [x.strip() for x in subprocess.check_output(
        ['git', 'status', '--porcelain']).split('\n') if x]
    return output


if __name__ == '__main__':
    # 'command, *args = sys.argv' on Python 3...
    command, args = sys.argv[0], sys.argv[1:]
    try:
        filename = args[-1]
        assert os.path.exists(filename)
    except (IndexError, AssertionError):
        print("git config --global core.editor {}".format(command))
        sys.exit(1)

    verbose = '-q' not in sys.argv
    if verbose:
        print('Press [Meta+Enter] or [Esc] followed by [Enter] to '
              'accept input.')
    with open(filename, 'r+') as file_obj:
        try:
            first_line = file_obj.readlines()[0].rstrip()
        except IndexError:
            # Empty file
            first_line = ''
        file_obj.seek(0)
        message = prompt('>> ', multiline=True)
        if not message and first_line:
            message = first_line
        file_obj.write(message)
        file_obj.truncate()

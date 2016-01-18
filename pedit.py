#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit import prompt
from prompt_toolkit.styles import PygmentsStyle
from pygments.token import Token

import os
import subprocess
import sys

toolbar_style = PygmentsStyle.from_defaults({
    Token.Toolbar: '#ffffff bg:#333333',
})


def get_toolbar(cli):
    toolbar_text = ('Press [Meta+Enter] or [Esc] followed by [Enter] to '
                    'accept input.')
    return [(Token.Toolbar, toolbar_text)]


def get_modified_files():
    files = [x.strip() for x in subprocess.check_output(
        ['git', 'status', '--porcelain']).split('\n') if x]
    if files:
        return WordCompleter(
            [x[2:].strip() for x in files if x.startswith('M')],
            ignore_case=True, WORD=True)


if __name__ == '__main__':
    # 'command, *args = sys.argv' on Python 3...
    command, args = sys.argv[0], sys.argv[1:]
    try:
        filename = args[-1]
        assert os.path.exists(filename)
    except (IndexError, AssertionError):
        print("git config --global core.editor {}".format(command))
        sys.exit(1)

    with open(filename, 'r+') as file_obj:
        try:
            first_line = file_obj.readlines()[0].rstrip()
        except IndexError:
            # Empty file
            first_line = ''
        file_obj.seek(0)
        modified_files = get_modified_files()
        if first_line and not first_line.startswith('#'):
            default = first_line
        else:
            default = ''
        try:
            message = prompt(
                '>> ', multiline=True, completer=modified_files,
                display_completions_in_columns=True,
                get_bottom_toolbar_tokens=get_toolbar,
                default='%s' % default,
                style=toolbar_style)
        except KeyboardInterrupt:
            sys.exit(1)
        if not message and first_line:
            message = first_line
        file_obj.write(message)
        file_obj.truncate()

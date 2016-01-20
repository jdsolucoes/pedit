#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import prompt
from prompt_toolkit.styles import PygmentsStyle
from pygments.token import Token

import os
import subprocess
import sys

toolbar_style = PygmentsStyle.from_defaults({
    Token.Toolbar: '#ffffff bg:#333333',
    Token.Branch: '#FF1A00 bg:#333333',
    Token.SCM: '#7072FF bg:#333333',
    Token.ADD: '#28FF1C'
})

# GIT COMMANDS
GIT_STATUS = ['git', 'status', '--porcelain']
GIT_BRANCH = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
GIT_MODIFICATIONS = ['git', '--no-pager',  'diff', '--numstat', 'HEAD']


def git_it(cmd):
    """Execute a GIT command and return the results"""
    return [x.strip() for x in subprocess.check_output(cmd).split('\n') if x]


def get_current_branch():
    """Get the branch name and some info for the toolbar"""
    branch_name = git_it(GIT_BRANCH)
    return branch_name[0]


def get_modifications():
    modifications = git_it(GIT_MODIFICATIONS)
    output = {}
    for modification in modifications:
        a, r, f = modification.split('\t')
        output[f] = (a, r)
    return output


class GitCompleter(Completer):

    def __init__(self, *args, **kwargs):
        files = git_it(GIT_STATUS)
        self.files = []
        self.modifications = get_modifications()
        for f in files:
            # its a addition
            if f.startswith('M') or f.startswith('A'):
                # modified file or added file
                self.files.append(f[2:].strip())
            elif f.startswith('R'):
                # renamed
                self.files.append(f[2:].replace('->', 'to').strip())
        super(GitCompleter)

    def get_completions(self, document, complete_event):
        word_before_cursor = document.text_before_cursor
        current_word = word_before_cursor.split(' ')[-1]
        for f in self.files:
            if f.startswith(current_word) and current_word:
                meta_info = self.modifications.get(f)
                if meta_info:
                    meta_msg = '%s insertions(+), %s deletions(-)' % meta_info
                else:
                    meta_msg = ''
                yield Completion(f, -len(current_word),
                                 display_meta=meta_msg)


def get_toolbar(cli):
    toolbar_text = ('Press [Meta+Enter] or [Esc] followed by [Enter] to '
                    'accept input. ')
    return [(Token.Toolbar, toolbar_text),
            (Token.SCM, 'git('),
            (Token.Branch, '%s' % get_current_branch()),
            (Token.SCM, ') ')]


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
        commit_lines = [x.strip() for x in file_obj.readlines()
                        if not x.startswith('#') and x]

        file_obj.seek(0)
        default = '\n'.join(commit_lines) if commit_lines else ''
        try:
            message = prompt(
                '>> ', multiline=True, completer=GitCompleter(),
                display_completions_in_columns=True,
                get_bottom_toolbar_tokens=get_toolbar,
                default='%s' % default,
                style=toolbar_style)
        except (KeyboardInterrupt, EOFError):
            sys.exit(1)
        file_obj.write(message)
        file_obj.truncate()

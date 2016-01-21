#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import prompt
from prompt_toolkit.styles import PygmentsStyle
from pygments.token import Token
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from datetime import datetime

import os
import subprocess
import sys

manager = KeyBindingManager.for_prompt()

toolbar_style = PygmentsStyle.from_defaults({
    Token.Toolbar: '#ffffff bg:#333333',
    Token.SCM: '#FF1A00 bg:#333333',
    Token.QUIT: '#ffffff bg:#ff0000'
})

# GIT COMMANDS
GIT_STATUS = ['git', 'status', '--porcelain']
GIT_BRANCH = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
GIT_MODIFICATIONS = ['git', '--no-pager',  'diff', '--numstat', 'HEAD']
GIT_AUTHORS = ["git", "log", "--format=%aN"]


@manager.registry.add_binding(Keys.ControlC)
@manager.registry.add_binding(Keys.ControlD)
def _(event):
    def quit_it():
        if getattr(event.cli, 'quit', False) is True:
            sys.exit(0)
        event.cli.quit = True
    event.cli.run_in_terminal(quit_it)


@manager.registry.add_binding(Keys.ControlG)
def show_git(event):
    def quit_it():
        event.cli.show_git = True
    event.cli.run_in_terminal(quit_it)


def git_it(cmd):
    """Execute a GIT command and return the results"""
    output = subprocess.check_output(cmd).decode('utf-8').split('\n')
    return [x.strip() for x in output if x]


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


def get_authors():
    authors = git_it(GIT_AUTHORS)
    return set(authors)


class GitCompleter(Completer):

    def __init__(self, *args, **kwargs):
        files = git_it(GIT_STATUS)
        self.files = []
        self.modifications = get_modifications()
        self.authors = get_authors()
        for f in files:
            # its a addition
            if f.startswith('M') or f.startswith('A'):
                # modified file or added file
                self.files.append(f[2:].strip())
            elif f.startswith('R'):
                # renamed
                self.files.append(f[2:].replace('->', 'to').strip())
        super(GitCompleter)

    def get_files(self, word_before_cursor, current_word):
        current_word = current_word[2:]
        for f in self.files:
            if f.startswith(current_word):
                meta_info = self.modifications.get(f)
                if meta_info:
                    meta_msg = '%s insertions(+), %s deletions(-)' % meta_info
                else:
                    meta_msg = ''
                yield Completion(f, -len(current_word) - 2,
                                 display_meta=meta_msg)

    def get_authors(self, word_before_cursor, current_word):
        current_word = current_word[1:]
        for f in self.authors:
            if f.startswith(current_word):
                yield Completion(f, -len(current_word) - 1)

    def get_completions(self, document, complete_event):
        word_before_cursor = document.text_before_cursor
        current_word = word_before_cursor.split(' ')[-1]
        if current_word.startswith('f:'):
            return self.get_files(word_before_cursor, current_word)
        elif current_word.startswith('@'):
            return self.get_authors(word_before_cursor, current_word)
        else:
            return []


def get_toolbar(cli):
    toolbar_text = ('Press [Meta+Enter] or [Esc] followed by [Enter] to '
                    'accept input. ')
    if getattr(cli, 'quit', False) is True:
        return [(Token.QUIT,
                 'Are you sure that you want to quit? press again')]
    if getattr(cli, 'show_git', False) is True:
        cli.show_git = False
        return [(Token.Toolbar, 'GIT Branch: '),
                (Token.SCM, '%s' % get_current_branch())]
    date = datetime.now().strftime('%d/%m/%Y %H:%M')
    return [(Token.Toolbar, toolbar_text),
            (Token.Toolbar, date)]


def get_title():
    return "Pedit!"


if __name__ == '__main__':
    # 'command, *args = sys.argv' on Python 3...
    command, args = sys.argv[0], sys.argv[1:]
    try:
        filename = args[-1]
        assert os.path.exists(filename)
    except (IndexError, AssertionError):
        print("git config --global core.editor {}".format(command))
        sys.exit(1)

    commit_lines = []
    with open(filename, 'r+') as file_obj:
        for line in file_obj.readlines():
            line = line.decode('utf-8').strip()
            if line and not line.startswith('#'):
                commit_lines.append(line)

        file_obj.seek(0)
        default = '\n'.join(commit_lines) if commit_lines else ''
        message = prompt(
            '>> ', multiline=True, completer=GitCompleter(),
            display_completions_in_columns=True,
            get_bottom_toolbar_tokens=get_toolbar,
            key_bindings_registry=manager.registry,
            get_title=get_title,
            default='%s' % default,
            enable_system_bindings=True,
            style=toolbar_style)

        file_obj.write(message)
        file_obj.truncate()

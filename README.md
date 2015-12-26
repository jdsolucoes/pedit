A simple yet usefull editor for short stuff, like commit messages.
In case you don't want a full-blown editor just to enter some text.

Only displays a new line on enter. Line edit functions are provided by GNU Readline.

## Pedit!
![Italian hand]
(http://static.memrise.com/uploads/course_photos/969204000140323231243.jpg)

How to install
==============

On bash:

```bash
# Recomended -- history, line edition and kill-ring (copy/paste)
pip install gnureadline
git clone https://github.com/jdsolucoes/pedit.git; cd pedit
sudo ln -s `pwd`/pedit.py /usr/bin/pedit
# Or just `pedit` -- without args, it outputs the git config command
git config --global core.editor pedit
```


On [fish](http://fishshell.com):

```fish
# Recomended -- history, line edition and kill-ring (copy/paste)
pip install gnureadline
git clone https://github.com/jdsolucoes/pedit.git; cd pedit
sudo ln -s (pwd)/pedit.py /usr/bin/pedit
eval (pedit) # to configure git
```

...and its done! Start commiting!

Configuration
=============

You can alter the [readline options](https://tiswww.case.edu/php/chet/readline/readline.html#SEC10)
by creating a `~/pedit.rc` file.

For example, the default editing mode is `emacs`. If you prefer vi-style keybindings:

```
set editing-mode vi
```

TODO
====

 * Integration with Mercurial, Bazaar, etc
 * Integration with the system's clipboard

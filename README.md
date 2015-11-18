A simple yet usefull one line editor for short commit messages


## Pedit!
![Italian hand]
(http://static.memrise.com/uploads/course_photos/969204000140323231243.jpg)

How to install
==============

```bash
pip install gnureadline # recomended
git clone https://github.com/jdsolucoes/pedit.git
cd pedit
sudo ln -s `pwd`/pedit.py /usr/bin/pedit
git config --global core.editor pedit
```

and its done!

Configuration
=============

You can alter the [readline options](https://tiswww.case.edu/php/chet/readline/readline.html#SEC10) 
by creating a `~/pedit.rc` file.

For example, the default editing mode is `emacs`. If you prefer vi-style keybindings:

```
set editing-mode vi
```

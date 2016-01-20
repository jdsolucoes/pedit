A simple yet usefull editor for short stuff, like commit messages.
In case you don't want a full-blown editor just to enter some text.

Only displays a new line on enter. Line edit functions are provided by [prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit)

## Pedit!
![Italian hand]
(http://static.memrise.com/uploads/course_photos/969204000140323231243.jpg)

How to install
==============

On bash:

```bash
pip install prompt-toolkit
git clone https://github.com/jdsolucoes/pedit.git; cd pedit
sudo ln -s `pwd`/pedit.py /usr/bin/pedit
# Or just `pedit` -- without args, it outputs the git config command
git config --global core.editor pedit
```


On [fish](http://fishshell.com):

```fish
pip install prompt-toolkit
git clone https://github.com/jdsolucoes/pedit.git; cd pedit
sudo ln -s (pwd)/pedit.py /usr/bin/pedit
eval (pedit) # to configure git
```

...and its done! Start commiting!

TODO
====

 * Integration with Mercurial, Bazaar, etc
 * Integration with the system's clipboard (yes, it's possible with readline)
 * Full featured support for pypy

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
git clone https://github.com/jdsolucoes/pedit.git; cd pedit
pip install -r requirements.txt
sudo ln -s `pwd`/pedit.py /usr/bin/pedit
`pedit` # to configure git
```


On [fish](http://fishshell.com):

```fish
git clone https://github.com/jdsolucoes/pedit.git; cd pedit
pip install -r requirements.txt
sudo ln -s (pwd)/pedit.py /usr/bin/pedit
eval (pedit) # to configure git
```

...and its done! Start commiting!

TODO
====

 * Integration with Mercurial, Bazaar, etc
 * Integration with the system's clipboard (yes, it's possible with readline)
 * Full featured support for pypy

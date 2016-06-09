Hey ya'll

The only compiled distribution I made was for Windows, so that's what you'll have to use.
Otherwise install python and the packages.

This "game" was built on the newest version of python (3.5+)
The game is dependant on the numpy (for faster C array manipulation) and pygame packages.

You can find the bleeding-edge pygame library .whl for python 3.5 here:
- http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame

Just extract and add folders to "python35 directory"/Lib/site-packages

Numpy can be installed with pip via shell. I recommend 32 bit python for this,
as the 64bit one had difficulty linking the C program for numpy during setup.py


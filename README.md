Detect Cars
===========

This project is a master's thesis that consisted of an investigation in the detection of cars and highway lines using Python and the OpenCV API.

System Requirements
-------------------
* An i3 or better processor.
* 2 GB or more RAM.
* At least 100 MB Free Disk space
* Windows 7 or later, OS X 10.8 or later (has only been tested on 10.9), Linux 3.0+

Installation
------------
1. First, one should install the following libraries:
  - OpenCV version 2.4.10+
  - Python 2.7.9 (or any later Python 2.x) ([See Installation on OS X if using a Mac](#installation-on-os-x))
  - Numpy 1.9.2+
  - Scipy 0.15.1+
- Now download and extract this repository with one of several options:
  - Cloning the repository with `git clone https://github.com/VAUTPL/Deteccion.git`
  - Download the repository as a .zip or .tar.gz and then extracting it.

Installation on OS X
--------------------
Apple uses a prior version of Python that does not support the latest Python libraries. One work around is to install Python with Homebrew:

`brew install python`

Replacing Apple's system Python with an unsupported version may break things. Therefore we linked Homebrew's python into the system path without replacing the system python:

`ln -s /usr/local/Cellar/python/2.x.y/bin/python /bin/hbpython`

Where 2.x.y is the version number of your Python.

Running
-------
From a command line in the folder of the repository:

`python detect.py [-v path/to/video] [-c path/to/cascade.xml]`

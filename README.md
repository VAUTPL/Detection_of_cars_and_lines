Detect Cars
===========

This project is a master's thesis that consisted of an investigation in the detection of cars and highway lines using Python and the OpenCV API. The code is free to be used and modified by anybody who wishes to do so.

System Requirements
-------------------
* An i3 or better processor. The faster the better, especially at high video resolutions.
* 2 GB or more RAM.
* At least 100 MB Free Disk space
* Windows 7 or later, OS X 10.8 or later (has only been tested on 10.9), Linux 3.0+

Installation
------------
1. First, one should install the following libraries:
  - [OpenCV](http://opencv.org/) version 2.4.10+
  - [Python](https://www.python.org/) 2.7.9 (or any later Python 2.x) ([See **_Installation on OS X_** if using a Mac](#installation-on-os-x))
  - [Numpy](http://www.numpy.org/) 1.9.2+
  - [Scipy](http://www.scipy.org/) 0.15.1+
- Now download and extract this repository with one of several options:
  - Clone the repository with `$ git clone https://github.com/VAUTPL/Deteccion.git`
  - Download the repository as a `.zip` or `.tar.gz` and then extract it.

Installation on OS X
--------------------
Apple uses a prior version of Python that does not support the latest Python libraries. One work around is to install Python with Homebrew:

`$ brew install python`

Replacing Apple's system Python with an unsupported version may break things. Therefore we linked Homebrew's Python into the system path without replacing the system Python:

`$ ln -s /usr/local/Cellar/python/2.x.y/bin/python /bin/hbpython`

Where 2.x.y is the version number of your Python.

Running
-------
From a command line in the folder of the repository:

`$ python detect.py [-v path/to/video] [-c path/to/cascade.xml]`

Or on UNIX, you may add a shebang (`#!`) line to the top of [detect.py](detect.py) with the path to the appropriate Python. Example:

`#! /bin/python` at the top of [detect.py](detect.py)

`$ chmod +x detect.py`

**To Run:**
`$ ./detect.py [-v path/to/video] [-c path/to/cascade.xml]`

If no video is specified, OpenCV attempts to open the Webcam, see line number 73:
`camera = cv2.VideoCapture(1)`
in [detect.py](detect.py)

###Other Arguments
Default values can be found in [config.py](config.py), but can be temporarily overwritten with the following arguments:
- **-c** or **--car** Path to Car Haar Cascade
- **-v** or **--video** Path to the (optional) video file -- default is Live Webcam Capture
- **-S** or **--scale-factor** Haar Cascade Scale Factor
- **-N** or **--min-neighbors** Haar Cascade Minimum Neighbors
- **DEPRECIATED:** _**-X** or **--roi-x** Region Of Interest top left corner X coordinate_
- **DEPRECIATED:** _**-Y** or **--roi-y** Region Of Interest top left corner Y coordinate_
- **DEPRECIATED:** _**-W** or **--roi-width** Region Of Interest Width_
- **DEPRECIATED:** _**-H** or **--roi-height** Region Of Interest Height_
- **-x** or **--max-line-gap** Max Line Gap
- **-n** or **--min-line-length** Min Line Length
- **-1** or **--threshold-1** Canny 1st Threshold
- **-2** or **--threshold-2** Canny 2nd Threshold
- **-a** or **--aperture-size** Canny Aperture Size
- **-r** or **--rho** Hough Rho
- **-t** or **--theta** Hough Theta in Radians
- **-T** or **--threshold** Hough Threshold
- **-D** or **--delay** Delay for operating system to sleep between frames, default is no delay (process as fast as possible)
- **-h** or **--help** Show help along with default values used for unspecified arguments

### Depreciated Arguments
Region of Interest is calculated based on the size of the video (full width, bottom half of the height). Therefore arguments which define the ROI are depreciated.

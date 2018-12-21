sgftokifu
==========================================

SGFtoKifu generates kifu diagrams from SGF files. It has been tested on windows
and linux, but should run on more platforms that have python.


Installation
============

In order to run SGFtoKifu you will need the following:

- Python Programming Language: available at http://www.python.org

- Python Imaging Library (PIL): available at http://www.pythonware.com/products/pil/

- typelib.py and sgflib.py from the Go Tools project, included in this package

- FreeSans.ttf font, also included in this package.

If you want, you can check out the Go Tools project page at 
http://gotools.sourceforge.net/ and the Free UCS Outline Fonts page (where the
FreeSans.ttf font came from) at http://savannah.nongnu.org/projects/freefont/.

After installing Python and PIL, just extract all the files in this package to a 
directory and you're all set.

If you have any problems, please contact me.


Usage
======
SGFtoKifu is a command line utility (for now). To run it with the default settings
just write:

python sgftokifu.py [name of the sgf file]

for example:
python sgftokifu.py kisei.sgf

To define options use the following syntax:
python sgftokifu.py [name of the sgf file] [option1 name=option1 value] 
 [option2 name=option2 value] ...

for example:
python sgftokifu.py kisei.sgf imagesize=800 fileformat=gif


The following options are available:

outputdir - the directory where to save the generated images
            default value: "."

fileformat - the format in which to save the generated images
             default value: "png"
             supported values: "png","gif","jpg"

filename - the name for the generated images
           default value: name of the sgf file

imagesize - base size of the image in pixels (the actual height of the
            image may be larger because of the text that needs to be
            appended to the end of the image)
            default value: 1000

spk - number of stones on each image
      default value: 100


To Do
=====

- Clean up and document the code

- Support for variations

- Support for comments (perhaps generate a pdf file instead of just the image)

- Pretty GUI

If you have any suggestions or want to help, please contact me!

Contact
=======

Project administrator: Manuel Cabral (manuel.cabral@gmail.com)
SGFtoKifu website: http://sgftokifu.sourceforge.net

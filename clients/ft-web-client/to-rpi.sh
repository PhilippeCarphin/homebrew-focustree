#!/bin/bash

cp ~/Dropbox/Notes/Notes_BUCKET/Notes_FocusTree.html build/help.html
rsync -av ./build/ apt-rpi:~/Documents/GitHub/FocusTree/clients/ft-web-client/build/

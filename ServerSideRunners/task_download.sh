#!/bin/bash

export PATH="/storage/brno2/home/previtus/anaconda2/bin:$PATH"
cd /auto/brno2/home/previtus/MGR-Project-Code/

#                   name fromId toId pixels
python run_downloader_on_server.py 1200x_markable_640x640 0 1200 640

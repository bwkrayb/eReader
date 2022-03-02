#!/bin/bash
export READER_HOME='/home/pi/reader'
cd $READER_HOME
nohup /usr/bin/python3 $READER_HOME/display.py > $READER_HOME/logs/start.out 2>&1 &

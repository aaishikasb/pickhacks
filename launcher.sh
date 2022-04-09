#!/bin/sh
# Navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/pickhacks
sudo python3 rpi-alexa.py
cd /
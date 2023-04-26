#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directoey, then execute python script, then back home

cd /
cd home/inia/phidget_indoor_project/modules
sudo python set_valves.py
cd /
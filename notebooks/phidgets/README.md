## README.md

December 6, 2023

This is a new implementation of the Phidget intro notebooks, which uses the "anywidget" library to talk to the USB devices.

The advantage of this is that it runs in Jupyter Classic Notebooks as well as Jupyter Lab and Jupyter 7.

Needs to use only certain browsers: Chrome, Chromium, Opera and Edge. Other browsers do not use WebUSB technology, so they will not work.

On a Raspberry Pi, use the latest OS (bookworm) in order for the anywidgets to work. Set up the udev rules for the R-Pi, as per the Phidgets webpages on setting up udev in Linux. 

The files ph4auto.js and ph4xx.css are required. They get loaded in by anywidgets.

You will need a Phidgets Starter Kit (with VINT, temperature/humidity sensor, two LEDs and two pushbuttons).

This is a test branch for using Phidgets with the "Anywidget" tool.

Latest test versions (Nov 23) works on both classic Jupyter notebooks as well as the  Callysto Lab enviroment. Test files are:
- PhidgetFour_auto.ipynb
- PhidgetFour_read.ipynb
- ph4auto.js, ph4read.js, ph4xx.css

To get to the "Jupyter Lab" environment, log into hub.callysto.ca and change the "tree" in the https address to "lab"

eg:

- https://hub-01.callysto.ca/jupyter/user/123ec456fg789hi012jkl/tree  change to
- https://hub-01.callysto.ca/jupyter/user/123ec456fg789hi012jkl/lab

There is a conditional install of the module "anywidget"

Successfully tested on:
- Mac OS in Chrome and Opera browsers
- Windows OS in Chrome browser
- Raspberry Pi in Chromium browser (latest OS and udev rules installed)

Important notes on Raspberry Pi:
- does not work with the old "buster" operating system
- does work on the latest operating system "bookworm". I have not tested others.
- it is important to install a file on the Raspberry Pi to allow access to the USB port.
- See the desciption here: [https://www.phidgets.com/docs/OS_-_Linux](https://www.phidgets.com/docs/OS_-_Linux)


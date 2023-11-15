This is a test branch for using Phidgets with the "Anywidget" tool.

Currently it DOES NOT WORK in the regular Callysto Hub, but it does work in the callysto Lab enviroment. 

To get to the "lab" environment, log into hub.callysto.ca and change the "tree" in the https address to "lab"

eg:

- https://hub-01.callysto.ca/jupyter/user/123ec456fg789hi012jkl/tree  change to
- https://hub-01.callysto.ca/jupyter/user/123ec456fg789hi012jkl/lab

You may also need to do a pip install. You can do this from the Jupyter notebook with the "! pip" command:
- ! pip install "anywidget[dev]"

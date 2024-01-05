## Notes on Phidget Samples

#### January 2024. Michael Lamoureux 

This folder contains several short notebooks showing how to use the Phidget devices. We have notebooks for:
- temperature
- humidity
- light level
- moisture level
- sound level
- slider
- sonar distance detector
- spatial orientation detector


We include two versions of each sample:
- basic (xxx_0.ipynb) which connects the device and shows a value. It has no error messages, to keep the code short.
- full (xxx.ipynb) which treats the device data as a "widget trait" that can be linked to another ipywidget on screen, using Python code. We might add error messages for debugging, but have not done this yet. The JS code could saved in a separate file; see the Plants notebooks for details.

- Maybe we don't need the first version. Should I delete them?

#### Programming notes

- we need to keep track of both the USB connection state, and the device channel state. Both need to be open in order for the software to communicate with the hardware. So there is some Boolean parameters used to track the state
- setting the data interval needs to be done asychronously. So in the OnAttach function, we make it async and add an "await" instruction to set the data
- each Phidget device has its own name for the parameter being monitored. Thus, the code has to be changed for each one. For instance: onHumidityChange(), onTemperatureChange(), onSPLChange(), etc. are the different code names to monitor when the data changes.
- the spatial Phidget returns 4 parameters corresponding to a quaternion, which is one way of representing an orientation in 3D. It can also directly return accleration, magnetic compass orientation, etc. This requires additional coding. 


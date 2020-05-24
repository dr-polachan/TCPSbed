# Changes

- Added support for slave side edge intelligence module
- Added support for master side edge intelligence module

# TCPSbed (v1.0) 

A Modular Testbed for Tactile Internet based Cyber-Physical Systems

![architecture](https://user-images.githubusercontent.com/48801729/76053561-9bfb7280-5f93-11ea-9f3b-4a4e6dd20639.png)

v1.0 (Description): Demonstrates basic testbed operation. Operator uses a USB mouse to control a robot simulated in VREP. Force feedback received from the robot side is printed at the ms-com terminal. Testbed components ms-com, srv, ss-com and embys-apps are run on different  hosts simulated in Mininet.

```diff
- Note: This is a demo version of TCPSbed. Only kinematic and haptic flows are supported in this version, support for other flows will be included soon. Only ms-embsys-app-mouseController and ss-embsys-vrep are supported in this version, support for other embsys-apps will be included soon.
```
# OS Requirement
Ubuntu 18.04

# Package Requirements
Python v2.7; mininet $sudo apt-get install mininet; ffmpeg, libav-tools $sudo apt-get install ffmpeg libav-tools
;pyaudio $sudo apt-get install python-pyaudio
;pyinput $sudo python -m pip install pynput==1.1.7 
;python-xlib $sudo apt-get install  python-xlib
;net-tools $sudo apt install net-tools
;libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 $sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
;pandas $sudo python -m pip install pandas
;pyserial $sudo python -m pip install pyserial
;xlrd $sudo python -m pip install xlrd
;opencv $sudo apt-get install python-opencv
;mss sudo python -m pip install mss==3.1.2
;scipy $pip install -U scipy
;scikits.bootstrap $pip install scikits.bootstrap
;sudo apt install libgl1-mesa-dev

# VREP Integration
VREP is a simulator platform for robots. For demonstration of the testbed we need to install VREP. First, download VREP v3.6.0 from https://www.coppeliarobotics.com/downloads and extract it to a folder. Next, update the parameter 'vrep_path' in TCPSbed/runDirectory/config to correspond to the path of the executable 'vrep.sh'

# Demonstration

## Testbed Component Placement (in Mininet)
- ms-embsys-app-mouseController is run on ms-com
- ss-embsys-app-vrep is run on ss-com
- To edit the delay, bandwidth and traffic of the links, change the default settings in the file TCPSbed/mininetScript/settings

![gitTestbedComponentPlacement](https://user-images.githubusercontent.com/48801729/75961647-65b4e900-5ee8-11ea-8c83-7cf4760f2347.png)

- To run the testbed, go to the folder mininetScript and run the command $sudo python mininetScript.py
- Wait for the xterm/windows ms-com, ss-com, srv, v-rep and ms-embsys-app-mouseController and ss-embsys-app-vrep to pop up
- Now use the mouse to control the PhantomX robot simulated in VREP
  - Right click the mouse to start the mouse control. Right click again to stop the mouse control
  - Mouse movements in X-Y direction is mapped to robot X-Y axis.  Y  movement  of  the  mouse,  while  the  left  button is pressed is mapped to the Z axis of the robot.
  - Use scroll wheel to open and close the pincher. 
- The force experienced by the robot when it hits an object is fedback to ms-com. The value is displayed in the ms-com terminal. 

![tcpsOperaton](https://user-images.githubusercontent.com/48801729/75965935-89c7f880-5eef-11ea-896b-19dbf08212e5.png)

# Publications
[1] Kurian Polachan, T Venkata Prabhakar, Chandramani Singh, Fernando A. Kuipers, "Towards an Open Testbed for Tactile Cyber Physical Systems", 11th 11th International Conference on COMmunication Systems & NETworkS, COMSNETS 2019 at Bangalore, India.


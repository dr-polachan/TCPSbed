# TCPSbed (v1.0) (Python Version Supported: 2.7)
A Modular Testbed for Tactile Internet based Cyber-Physical Systems

v1.0 (Description): Demonstrates basic testbed operation. Operator uses a USB mouse to control a robot simulated in VREP. Force feedback received from the robot side is printed at the ms-com terminal. Testbed components ms-com, srv, ss-com and embys-apps are run on different  hosts simulated in Mininet.

Notice: Only kinematic and haptic flows are supported, support to other flows will be added soon. Only ms-embsys-app-mouseController and ss-embsys-vrep is supported in this version, support to other embsys-apps will be added soon.

# Package Requirements
ffmpeg, libav-tools $sudo apt-get install ffmpeg libav-tools
;pyaudio $sudo pip install pyaudio
;pyinput $sudo python -m pip install pynput = 1.1.7 
;python-xlib $sudo apt-get install  python-xlib
;net-tools $sudo apt install net-tools
;libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 $sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
;pandas $sudo python -m pip install pandas
;pyserial $sudo python -m pip insatll pyserial
;xlrd $sudo python -m pip install xlrd
;opencv $sudo apt-get install python-opencv
;mss sudo python -m pip install mss
;scipy $pip install -U scipy
;scikits.bootstrap $pip install scikits.bootstrap

# Testbed Component Placement (in Mininet)
- ms-embsys-app-mouseController is run on ms-com
- ss-embsys-app-vrep is run on ss-com
- To edit the delay, bandwidth and traffic of the links, change the default settings in the file TCPSbed/mininetScript/settings

![gitTestbedComponentPlacement](https://user-images.githubusercontent.com/48801729/75961647-65b4e900-5ee8-11ea-8c83-7cf4760f2347.png)

# Demonstration
- To run the testbed, go to the folder mininetScript and run the command $sudo python mininetScript.py
- Wait for the xterm/windows ms-com, ss-com, srv, VREP and ms-embsys-app-mouseController and ss-embsys-app-vrep to pop up
- Now use the mouse to control the PhantomX robot simulated in VREP
  - Right click the mouse to start the mouse control. Right click again to stop the mouse control
  - Mouse movements in X-Y direction is mapped to robot X-Y axis.  Y  movement  of  the  mouse,  while  the  left  button is pressed is mapped to the Z axis of the robot.
  - Use scroll wheel to open and close the pincher. 
- The force experienced by the robot when it hits an object is fedback to ms-com. The value is displayed in the ms-com terminal. 

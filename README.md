# TCPSbed (v1.0) (Python Version Supported: 2.7)
A Modular Testbed for Tactile Internet based Cyber-Physical Systems

v1.0 (Description): Demonstrates basic testbed operation. Operator uses a USB mouse to control a robot simulated in VREP. Force feedback received from the robot side is printed at the ms-com terminal. Testbed components ms-com, srv, ss-com and embys-apps are run on different  hosts simulated in Mininet.

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
- embsys-app ms-embsys-app-mouseController is run on ms-com
- embsys-app ss-embsys-app-vrep is run on ss-com
- the delay, bandwidth and traffic in the links can be parameterized by editing the file TCPSbed/mininetScript/settings

![gitTestbedComponentPlacement](https://user-images.githubusercontent.com/48801729/75961647-65b4e900-5ee8-11ea-8c83-7cf4760f2347.png)


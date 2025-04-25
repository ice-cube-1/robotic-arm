# Semi-autonomous robotic arm with digital twin

View the full project writeup [here](https://github.com/ice-cube-1/robotic-arm/blob/main/writeup.pdf)

## Summary

![](https://github.com/ice-cube-1/robotic-arm/blob/main/readme_images/arm_white_bg.png)

The overall aim for this project is to design a high precision robotic arm and provide easy to use controls for it, including some autonomous capabilities. An important part of this is the digital twin, which I have implemented as a 3D render of the arm’s current position and has various positioning controls. The project also has a substantial computer vision aspect, with object and colour detection to produce size and position calculations. The objects are then rendered in their position relative to the arm, with the option to pick them up. The final major software aspect is writing scripts, meaning that the user can write programs in a simple format to control the arm autonomously.

The arm itself is designed in Fusion 360 and 3D printed, controlled by an Arduino and powered with various servos and steppers. This is connected to a raspberry Pi, which hosts a Python webserver that sends commands to the Arduino over a Serial port and creates a WebSocket connection to the HTML that it also serves. The rendering is done using WebGL and TypeScript, and the documentation for writing scripts is also served by the python webserver, written with markdown and formatted using MkDocs.

Real position of the arm          |  Rendered position
:-------------------------:|:-------------------------:
![](https://github.com/ice-cube-1/robotic-arm/blob/main/readme_images/irl.jpg)  |  ![](https://github.com/ice-cube-1/robotic-arm/blob/main/readme_images/virtual.jpg)

## Diagrams

![](https://github.com/ice-cube-1/robotic-arm/blob/main/readme_images/data_flow_diagram.png)\
Data flow diagram


![](https://github.com/ice-cube-1/robotic-arm/blob/main/readme_images/flowchart.png)\
Flowchart

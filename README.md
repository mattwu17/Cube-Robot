<h1 align="center">Cube-Robot</h1>

<h2 align="center">A robot that solves Rubik's Cubes</body>

https://user-images.githubusercontent.com/69494421/128615952-5cfed673-b55f-4ff5-a4c2-c13ca85e1fac.mp4

(A random shuffle followed by an automated solve)

# Table of Contents

- [Description](#description)
- [Design](#design)
  *  [Wiring](#wiring)
  * [Required Libraries](#required-libraries)
  * [Bill of Materials](#bill-of-materials)
- [Executing program](#executing-program)
- [Acknowledgments](#acknowledgments)


## Description

Okay, a here's a more in-depth description. This cube-solving robot is made with dozens of 3D printed parts, 6 NEMA-17 stepper motors, 6 NeoPixel ring lights, 2 webcams, a Raspberry Pi, and an Arduino Uno.

The brain of the project is the Raspberry Pi, which runs the Python script which contains the commands for reading the faces of the cube and solving the cube. The Pi connects to a slave Arduino Uno via USB serial connection, sending instructions to turn the lights on/off. The Pi connects directly to drivewrs for all 6 steper motors, which each control their respective stepper motors. The Pi also connects to both webcams via USB, which are used to read the faces of the cube.

## Design

When designing the robot, there were a few specifications that I designed around:
* The robot must be able to detect all colors automatically
  * No holding the cube in front of a camera face-by-face
* The user must be able to take the cube in and out of the robot
* The user must be able to see the cube while it is being solved 

To create a program that could automatically detect all of the colors of the cube, I decided to use OpenCV in conjunction with two USB webcams. This way, the machine would be able to observe all six sides of the cube without having to rotate it (each camera sees three sides).

In order to accomodate the cube being taken both in and out of the robot, I modified a normal Rubik's Cube by carving slots in the center of each face for the rotating motor arm to latch onto. To load the cube in, the top hat can simply be removed and each arm can be pulled back slightly to allow room for the cube to slide in.

In order for users to see the cube being solved, the robot must be exposed to room lighting conditions, which are not entirely uniform. To avoid the use of a surrounding enclosure, I instead opted to add additional lighting that would ensure a consistent state for each time the robot operates.


![Initial Prototype](https://user-images.githubusercontent.com/69494421/128763846-3408e5c4-86d6-4745-9285-f835e43ab5b2.png)

This is the initial prototype for the robot. The prototype uses a thinner support for the top motor and slightly less supportive holders for the side motors. In the final version, the top motor holder is made thicker in order to shield the cube from room lighting conditions as much as possible. Additionally, the supports for the side motors have been modified to allow for easier storage of motor wires and mounting of lights.

## Wiring

The wiring for the robot is divided into two separate areas. The first board contains 6 stepper motor drivers, as well as connections to the 12V 10A power supply used to power the stepper motors. To make this board, I tried to solder. This was my first attempt soldering a board this intricate, and with my $20 Microcenter soldering iron I stood no chance. The second board contains a breadboard along with an Arduino Uno. After the first board, I knew if I soldered it, I would never get it to work right.

![IMG_5703](https://user-images.githubusercontent.com/69494421/128765387-05e6a50c-ba14-46b3-a628-18b527d0e971.jpg)
The final version of the board (above), Frustration with the soldering process (below)
![Soldering is hard...](https://user-images.githubusercontent.com/69494421/128764859-9deaaa1d-2959-410d-819c-987d3575b329.jpeg)


## Required Libraries

To simplify this project, I relied on the use of other libraries. Most notably, I am using the Kociemba library which contains an algorithm for solving cubes that takes the state of a scrambled cube as an imput and outputs the shortest list of moves that will solve the cube.

* Kociemba (efficient solution algorithm)
```
pip install kociemba
```
* OpenCV (camera vision)
```
pip install opencv-python
```
* Numpy (matrices used with OpenCV)
```
pip install numpy
```

## Bill of Materials

Part No. | Name | Count | Price
--- | --- | --- | ---
1 | USB Camera | 2 | $9.99 
2 | NeoPixel Ring | 6 | $4.99
3 | NEMA 17 Stepper Motor | 6 | $9.49
4 | Stepper Motor Driver | 6 | $1.33
5 | 12V 10A Power Supply | 1 | $19.86
6 | Rubik's Cube | 1 | $5.99
7 | Raspberry Pi 3 B+ | 1 | $34.99
8 | Arduino Uno | 1 | $23.00
9 | 3D Printer Filament: 1kg | 1 | $16.99
TOTAL | --- | --- | $215.67


## Executing program

The executable portion of the project lies within a Python script, cube_solver.py. The script runs through a series of smaller steps:

### Declaring constants
This script uses a significant number of constants for the cameras to detect the colors on the cube. The constants defined are the coordinates of the center of each face, as well as HSV color ranges for each color on each camera.

### Initializing the Cameras and Taking Snapshots
The script begins by creating video capture objects for both of the cameras. The Raspberry Pi then sends serial information to the Arduino, instructing it to turn specified lights on and off so that photos can be taken. In total, the cameras capture 3 pictures for analysys: one in white light for the top and bottom camera, and one in blue light for the top camera.

### Creating Masks and Analyzing Snapshots
After capturing images of all sides of the cube, the script creates masks for each color being analyzed using the input color ranges. Each color receives a binary mask where pixels within the specified range of colors are selected. After creating these masks, the script iterates along the list of coordinates that mark the centers of each color square. A conditional block detects which color is present at each coordinate and appends an identifier character for each color to a string. Once the entire cube has been identified, the script performs string manipulation to make the format compatable with the Kociemba library.

### Moving the Cube
Control of the six stepper motors is handled by the Pi. A separate file, stepper.py, contains functions to initiate and turn each motor. The main script uses these functions to iterate through the list of instructions and turn the specified amount each time. 

After the final step, the script is complete and the cube will be solved. :)


## Acknowledgments

Inspiration, code snippets, etc.
* [Kociemba Library](https://pypi.org/project/kociemba/)
* [OpenCV Tutorials](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html)
* [Pi/Arduino Communications](https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/)

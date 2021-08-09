# Cube Robot

It's pretty straight forward, I made a robot that solved Rubik's cubes.

https://user-images.githubusercontent.com/69494421/128615952-5cfed673-b55f-4ff5-a4c2-c13ca85e1fac.mp4

(A random shuffle followed by an automated solve)

## Description

Okay, a here's a more in-depth description. This cube-solving robot is made with dozens of 3D printed parts, 6 NEMA-17 stepper motors, 6 NeoPixel ring lights, 2 webcams, a Raspberry Pi, and an Arduino Uno.

The brain of the project is the Raspberry Pi, which runs the Python script which contains the commands for reading the faces of the cube and solving the cube. The Pi connects to a slave Arduino Uno via USB serial connection, sending instructions to turn the lights on/off. The Pi connects directly to drivewrs for all 6 steper motors, which each control their respective stepper motors. The Pi also connects to both webcams via USB, which are used to read the faces of the cube.

## Design

When designing the robot, there were a few specifications that I designed around:
* The robot must be able to detect all colors automatically
  * No holding the cube in front of a camera face-by-face
* The user must be able to take the cube in and out of the robot
* The user must be able to see the cube while it is being solved 

### Required Libraries

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

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets


## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)

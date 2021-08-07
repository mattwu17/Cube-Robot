'''
This file contains functions to control the motion of the six stepper
motors used by the Rubiks Cube solver. The pins associated with each
motor are stored at matching indices of step and direction arrays.
'''

from time import sleep
import RPi.GPIO as GPIO

DELAY = 0.001
# CW / CCW are relative to the CUBE
CW = 0
CCW = 1
SPT = 50           # steps per turn, or steps per rotation / 4

DIR = [21,16,1,25,24,15] 
STEP = [20,12,7,8,23,18]

faces = dict(U = 3, R = 1, F = 5, D = 4, L = 2, B = 0)

def setup():
    # setup pins on RPi
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    for i in range(6):
        GPIO.setup(DIR[i], GPIO.OUT)
        GPIO.setup(STEP[i], GPIO.OUT)
        GPIO.output(DIR[i], CW)
    
def turn(instr):
    # gets the current pins and face of current instruction
    face_char = instr[0]
    curr_face = faces[face_char]
    curr_dir = DIR[curr_face]
    curr_step = STEP[curr_face]
    
    if "'" in instr:
        GPIO.output(curr_dir, CCW)
    else:
        GPIO.output(curr_dir, CW)
    
    if "2" in instr:
        num_turns = 2
    elif instr == "D'":
        num_turns = 3
    else:
        num_turns = 1
    
    for i in range(SPT * num_turns):
        GPIO.output(curr_step, GPIO.HIGH)
        sleep(DELAY)
        GPIO.output(curr_step, GPIO.LOW)
        sleep(DELAY)
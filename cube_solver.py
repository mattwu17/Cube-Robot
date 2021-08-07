import cv2
import numpy as np
import time
import serial
import kociemba
import stepper

########## CONSTANTS ##########

# ALL VARIABLES PRECEEDED WITH "t_" INDICATE THEY ARE FOR TOP CAM, "b_" FOR BOTTOM CAM
t_coord_list = [(329,45),(362,67),(428,101),(247,62),(299,107),(368,128),(178,90),(231,124),(299,165),(333,241),(404,190),(457,161),(332,310),(379,256),(445,223),(327,364),(385,319),(445,262),(145,150),(197,187),(257,237),(157,215),(214,252),(261,307),(157,257),(209,314),(263,366)]
b_coord_list = [(440,304),(387,332),(356,353),(397,277),(333,293),(285,332),(332,241),(274,277),(227,307),(361,65),(412,102),(466,155),(362,113),(405,161),(466,190),(367,177),(427,220),(475,253),(203,159),(251,106),(303,63),(203,194),(258,163),(300,116),(197,256),(240,222),(296,179)]

# RANGES FOR MASKS
# orange has HSV hue value that wraps around circle, so we have 2 masks
t_lower_red = np.array([150,110,110])
t_upper_red = np.array([179,255,255])
t_lower_orange = np.array([0,20,10])
t_upper_orange = np.array([20,255,255])
t_lower_orange_2 = np.array([130,0,170])
t_upper_orange_2 = np.array([179,255,255])
t_lower_green = np.array([80,100,50])
t_upper_green = np.array([93,255,255])
t_lower_blue = np.array([95,225,225])
t_upper_blue = np.array([115,255,255])
t_lower_white = np.array([93,0,254])
t_upper_white = np.array([130,255,255])

b_lower_red = np.array([145,128,120])
b_upper_red = np.array([179,255,245])
b_lower_green = np.array([70,200,100])
b_upper_green = np.array([93,255,255])
b_lower_blue = np.array([94,160,100])
b_upper_blue = np.array([118,255,255])
b_lower_white = np.array([94,0,254])
b_upper_white = np.array([130,255,255])
b_lower_yellow = np.array([63,0,0])
b_upper_yellow = np.array([103,255,255])

########## CODE ##########

def main():
    # ser used to communicate with Arduino
    ser = serial.Serial(port='/dev/ttyACM0',baudrate = 9600,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)

    # creates a cam object
    b_cam = cv2.VideoCapture(0)
    t_cam = cv2.VideoCapture(2)
    
    # try-except block across whole code
    try:
        ########## IMAGE CAPTURE ##########
        
        # "warms up" serial connection once before beginning
        ser.write(b'D')
        time.sleep(1)
        
        # gets a lit frame
        ser.write(b'D')
        ser.write(b'T')
        for i in range(50):
            _, t_lit_frame = t_cam.read()
        
        # gets a blue frame
        ser.write(b'M')
        for i in range(50):
            _, t_blue_frame = t_cam.read()
        
        # turns off the lights when they are no longer needed
        ser.write(b'Y')
        
        # gets a lit frame
        ser.write(b'B')
        for i in range(50):
            _, b_lit_frame = b_cam.read()
        
        # turns off the lights when they are no longer needed
        ser.write(b'X')
        
        ########## IMAGE PROCESSING ##########
        
        # convert all frames to HSV
        t_hsv_lit = cv2.cvtColor(t_lit_frame, cv2.COLOR_BGR2HSV)
        t_hsv_blue = cv2.cvtColor(t_blue_frame, cv2.COLOR_BGR2HSV)
        b_hsv_lit = cv2.cvtColor(b_lit_frame, cv2.COLOR_BGR2HSV)
        
        # create a new mask for every color we will detect
        t_red_mask = cv2.inRange(t_hsv_lit, t_lower_red, t_upper_red)
        t_orange_mask = cv2.inRange(t_hsv_lit, t_lower_orange, t_upper_orange)
        t_orange_mask_2 = cv2.inRange(t_hsv_lit, t_lower_orange_2, t_upper_orange_2)
        t_green_mask = cv2.inRange(t_hsv_lit, t_lower_green, t_upper_green)
        t_blue_mask = cv2.inRange(t_hsv_lit, t_lower_blue, t_upper_blue)
        t_white_mask = cv2.inRange(t_hsv_blue, t_lower_white, t_upper_white)
        b_red_mask = cv2.inRange(b_hsv_lit, b_lower_red, b_upper_red)
        b_green_mask = cv2.inRange(b_hsv_lit, b_lower_green, b_upper_green)
        b_blue_mask = cv2.inRange(b_hsv_lit, b_lower_blue, b_upper_blue)
        b_white_mask = cv2.inRange(b_hsv_lit, b_lower_white, b_upper_white)
        b_yellow_mask = cv2.inRange(b_hsv_lit, b_lower_yellow, b_upper_yellow)
        
        # writes images to file, useful for debugging
        """
        cv2.imwrite("t_redmask.png",t_red_mask)
        cv2.imwrite("t_orangemask.png",t_orange_mask)
        cv2.imwrite("t_orangemask2.png",t_orange_mask_2)
        cv2.imwrite("t_greenmask.png",t_green_mask)
        cv2.imwrite("t_bluemask.png",t_blue_mask)
        cv2.imwrite("t_whitemask.png",t_white_mask)
        cv2.imwrite("t_blue.png", t_blue_frame)
        cv2.imwrite("t_white.png", t_lit_frame)
        cv2.imwrite("b_redmask.png",b_red_mask)
        cv2.imwrite("b_greenmask.png",b_green_mask)
        cv2.imwrite("b_bluemask.png",b_blue_mask)
        cv2.imwrite("b_whitemask.png",b_white_mask)
        cv2.imwrite("b_yellowmask.png", b_yellow_mask)
        cv2.imwrite("b_white.png", b_lit_frame)
        """

        ########## LOGIC / COLOR IDENTIFICATION ##########
        """
        FOR THE SOLVING ALGORITHM, WE NEED A SPECIAL FORMAT
        
        RED (R)       -> 1
        ORANGE (O)    -> 2
        GREEN (G)     -> 3
        BLUE (B)      -> 4
        YELLOW (Y)    -> 5
        WHITE (W)     -> 6
        
        CONVERT TO:
        UP (U)
        RIGHT (R)
        FRONT (F)
        DOWN (D)
        LEFT (L)
        BACK (B)
        """
        cube = ""
        
        # logic for getting colors from top faces
        for (coord2, coord1) in t_coord_list:
            if t_red_mask[coord1,coord2] == 255:
                cube += '1'
                print('R')
            elif t_orange_mask[coord1,coord2] == 255 or t_orange_mask_2[coord1, coord2] == 255:
                cube += '2'
                print('O')
            elif t_green_mask[coord1,coord2] == 255:
                cube += '3'
                print('G')
            elif t_blue_mask[coord1,coord2] == 255:
                cube += '4'
                print('B')
            elif t_white_mask[coord1,coord2] == 255:
                cube += '5'
                print('W')
            else:
                cube += '6'
                print('Y')
        
        # logic for getting colors from bottom faces
        # numbers out of order for logic reasons
        for (coord2, coord1) in b_coord_list:
            if b_red_mask[coord1,coord2] != 0:
                cube += '1'
                print('R')
            elif b_green_mask[coord1,coord2] != 0:
                cube += '3'
                print('G')
            elif b_blue_mask[coord1,coord2] != 0:
                cube += '4'
                print('B')
            elif b_white_mask[coord1,coord2] != 0:
                cube += '5'
                print('W')
            elif b_yellow_mask[coord1,coord2] != 0:
                cube += '6'
                print('Y')
            else:
                cube += '2'
                print('O')
        
        # hash map to convert colors into faces for algorithm
        convert = {'U': cube[4],
                   'R': cube[13],
                   'F': cube[22],
                   'D': cube[31],
                   'L': cube[40],
                   'B': cube[49]}
        
        cube = cube.replace(convert['U'], 'U')
        cube = cube.replace(convert['R'], 'R')
        cube = cube.replace(convert['F'], 'F')
        cube = cube.replace(convert['D'], 'D')
        cube = cube.replace(convert['L'], 'L')
        cube = cube.replace(convert['B'], 'B')
        
        ########## MOVING THE MOTORS ##########
        
        # this is where it will get the orientation of the cube
        stepper.setup()
        
        # generate optimal solution for cube
        solved = kociemba.solve(cube)
        
        instrs = solved.split()
        
        # completes all instructions
        for x in instrs:
            stepper.turn(x)

    except KeyboardInterrupt:
        exit()
        
    print("complete")

    t_cam.release()
    b_cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
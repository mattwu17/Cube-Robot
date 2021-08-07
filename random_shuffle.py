import stepper
import random

def main():
    stepper.setup()
        
    for i in range(50):
        instr = ""
        faces = ['U','R','F','D','L','B']
        instr += faces[random.randint(0,5)]
            
        if random.randint(0,1) == 0:
            instr += "'"
            
        stepper.turn(instr)
    
if __name__ == "__main__":
    main()
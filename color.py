#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

##--##--##--## ROBO CONSTANTS ##--##--## 
import RoboConstants as RC

##--##--##--## CODE CONSTANTS ##--##--##--##
import CodeCostants as CC

##--##--##--## ROBO SET UP ##--##--## 
Ev3 = EV3Brick()

# Motors
SortingMotor = Motor( RC.Motors['sort'],positive_direction = Direction.COUNTERCLOCKWISE )
LeftMotor = Motor( RC.Motors['left'],positive_direction = Direction.COUNTERCLOCKWISE )

# Sensors
ColorSensor = ColorSensor( RC.ColorSensor_port )

FrontBtn = TouchSensor( RC.Buttons['front'] )

##--##--##--## CHECKING THE COLORS ##--##--## 

# sorts the ping pong balls based on highest rgb value - red or blue
def Sort_Func( DetectedColor, sort ):
    Sorting = True

    print(sort)
    if sort:
        if DetectedColor == Color.RED:
            print('red')
            SortingMotor.run_angle(CC.SortingSpeed, CC.SortAngle['red'], then=Stop.HOLD, wait=False)
            Now_Sorting = True

        elif DetectedColor == Color.BLUE:
            print('blue')
            SortingMotor.run_angle(CC.SortingSpeed, CC.SortAngle['blue'], then=Stop.HOLD, wait=False)
            Now_Sorting = True
        else:
            print("unknown color: ", DetectedColor)
    else:
        # no need to sort by color - balls are just picked up into the same container to be throwed on oponent's side  
        SortingMotor.run_angle(CC.SortingSpeed, CC.SortAngle['red'], then=Stop.HOLD, wait=False)


##--##--##--## GAME LOOP ##--##--##--##
Now_Sorting = False
#LeftMotor.run(CC.DriveSpeed)

while True:
    # color detection
    DetectedColor = ColorSensor.color()

    if DetectedColor != None and not Now_Sorting:
        print('next up: sort func')
        Sort_Func( DetectedColor, CC.Do_ColorSort )

    elif DetectedColor == None:
        Now_Sorting = False
    

    # break the loop
    if FrontBtn.pressed():
        LeftMotor.stop()
        break
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
RightMotor = Motor( RC.Motors['right'],positive_direction = Direction.COUNTERCLOCKWISE )

# Sensors
ColorSensor = ColorSensor( RC.ColorSensor_port )

FrontBtn = TouchSensor( RC.Buttons['front'] )

##--##--##--## CHECKING THE COLORS ##--##--## 

# sorts the ping pong balls
def Sort_Func( DetectedColor, sort ): # sorts the ping pong balls
    global Now_Sorting, Back_Direction
    if sort:
        if DetectedColor == Color.RED:
            Now_Sorting = True
            
            print('red')
            SortingMotor.run_angle(
                CC.SortSpeed,
                CC.SortAngle['red'],
                then=Stop.BRAKE,
                wait=False
            )
            Back_Direction = 'red'

        elif DetectedColor == Color.BLUE:
            Now_Sorting = True
            
            print('blue')
            
            SortingMotor.run_angle(
                CC.SortSpeed,
                CC.SortAngle['blue'],
                then=Stop.BRAKE,
                wait=False
            )
            Back_Direction = 'blue'
        else:
            print("ERROR: unknown color: ", DetectedColor) # quite common - TODO: OPT change sth to make it rarer
            Now_Sorting = False
    else:
        Now_Sorting = True
        
        print('part 2 sort')
        # no need to sort by color - balls are just picked up into the same container to be throwed on oponent's side  
        SortingMotor.run_angle(CC.SortSpeed, CC.SortAngle['red'], then=Stop.BRAKE, wait=False)

##--##--##--## GAME LOOP ##--##--##--##
Now_Sorting = False
Back_Direction = None

while True:
    # color detection
    DetectedColor = ColorSensor.color()
    if DetectedColor != None and not Now_Sorting:
        Sort_Func( DetectedColor, CC.Do_ColorSort )

    if Now_Sorting:
        if Back_Direction:
            if abs(SortingMotor.angle()) >= abs(CC.SortAngle[Back_Direction]) - CC.SortToleration:

                SortingMotor.run_angle(
                    CC.SortSpeed,
                    -1* CC.SortAngle[Back_Direction], # the second part makes the motor move on the way back a bit less
                    then=Stop.BRAKE,
                    wait=False
                )
                print('changing sort direction')

                Back_Direction = None
            else:
                print(abs(SortingMotor.angle()) - abs(CC.SortAngle[Back_Direction]))
        elif not Back_Direction:
            if abs(SortingMotor.angle()) <= CC.SortToleration:
                SortingMotor.brake()
                print('sorting finished')
                Now_Sorting = False


    
    # break the loop
    if FrontBtn.pressed():
        #RightMotor.stop()
        break
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

# sorts the ping pong balls based on highest rgb value - red or blue
def Sort_Func( DetectedColor, sort ):
    global Now_Sorting, Back_Direction
    if int(Clock.time()) != 0:
       print("we have a problem with Stopwatch not being at zero after a pause and reset, for easier debuging here is the time: ", Clock.time())
    
    if sort:
        if DetectedColor == Color.RED:
            Clock.resume()
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
            Clock.resume()
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
            print("ERROR: unknown color: ", DetectedColor) # quite common - TODO: change sth to make it rarer
            Now_Sorting = False
    else:
        Clock.resume()
        Now_Sorting = True
        
        print('part 2 sort')
        # no need to sort by color - balls are just picked up into the same container to be throwed on oponent's side  
        SortingMotor.run_angle(CC.SortSpeed, CC.SortAngle['red'], then=Stop.BRAKE, wait=False)

##--##--##--## Other func ##--##--##--##
def sign(a): # return a mathematical sign of a given number ( + 0 - )
    a = int(a)
    if a == 0:
        return 0
    elif a > 0:
        return -1
    else:
        return 1

##--##--##--## GAME LOOP ##--##--##--##
Now_Sorting = False
Back_Direction = None
Clock = StopWatch()
Clock.pause()
Clock.reset()
# RightMotor.run(int(CC.DriveSpeed/2))

while True:
    # color detection
    DetectedColor = ColorSensor.color()

    if DetectedColor != None and not Now_Sorting:
        Sort_Func( DetectedColor, CC.Do_ColorSort )

    if Now_Sorting and int(Clock.time()) > CC.SortTime:
        if Back_Direction:
            print('changing in time: ', Clock.time(), ' now going to starting place')
            Clock.reset()

            SortingMotor.run_angle(
                CC.SortSpeed,
                -1* CC.SortAngle[Back_Direction] + sign(CC.SortAngle[Back_Direction])*5, # the second part makes the motor move on the way back a bit less
                then=Stop.BRAKE,
                wait=False
            )
            Back_Direction = None
        else:
            Clock.pause()
            print('changing bool "Now_Sorting" in time: ', Clock.time())
            Clock.reset()

            Now_Sorting = False

    
    # break the loop
    if FrontBtn.pressed():
        #RightMotor.stop()
        break
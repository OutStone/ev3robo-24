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

DetectedColor = ColorSensor.color()
print(DetectedColor)

print('red')
SortingMotor.run_angle(
    CC.SortSpeed,
    CC.DropPoints['red'],
    then=Stop.BRAKE,
    wait=True
)
wait(1000)

SortingMotor.run_angle(
    CC.SortSpeed,
    CC.DropPoints['red'] * -1,
    then=Stop.BRAKE,
    wait=True
)


print('blue')

SortingMotor.run_angle(
    CC.SortSpeed,
    CC.DropPoints['blue'],
    then=Stop.BRAKE,
    wait=True
)
wait(1000)

SortingMotor.run_angle(
    CC.SortSpeed,
    CC.DropPoints['blue'] * -1,
    then=Stop.BRAKE,
    wait=True
)
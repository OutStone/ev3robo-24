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
RightMotor = Motor( RC.Motors['right'],positive_direction = Direction.COUNTERCLOCKWISE )
robot = DriveBase( LeftMotor, RightMotor, RC.Wheel_Diameter, RC.Axle_Track )


FrontBtn = TouchSensor( RC.Buttons['front'] )


robot.drive(200,0)
wait(10000)
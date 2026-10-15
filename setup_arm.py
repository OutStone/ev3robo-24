#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

##--##--##--## ROBO CONSTANTS ##--##--## 
import constants_robo as RC

##--##--##--## CODE CONSTANTS ##--##--##--##
import constants_code as CC

ArmMotor = Motor( RC.Motors['arm'],positive_direction = Direction.CLOCKWISE )
btn = TouchSensor(RC.Buttons['1'])
Ev3 = EV3Brick()

# rotation reverse
d = 1
if input('unempty input = direction inward:') != "":
    d = -1

# rotation 'till btn press
while not btn.pressed():
    ArmMotor.run(d*360)

ArmMotor.hold()
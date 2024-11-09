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

FrontBtn =  TouchSensor( RC.Buttons['front'] )
Gyro = GyroSensor( RC.Gyro_port )
#UlraSensor = UltrasonicSensor( RC.UlraSensor_port )

Ev3.speaker.beep()
while True:
    #dist = UlraSensor.distance()
    angle = Gyro.angle()
    print(angle)
    if FrontBtn.pressed():
        break

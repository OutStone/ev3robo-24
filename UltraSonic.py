#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

##--##--##--## ROBo - CONSTANTS ##--##--## 
from RoboConstants.py import ( Motors, Buttons, ColorSensor_port,
                                Wheel_Diameter, Axle_Track, InfraSensor_port )
# TODO: test if I can just import the file without specifing the variables to be imported
RUN = True

##--##--##--## CODE CONSTANTS ##--##--##--##
import CodeConstants

##--##--##--## ROBO SETT UP ##--##--## 
Ev3 = EV3Brick()

# Motors
LeftMotor = Motor( Motors['left'],positive_direction = Direction.COUNTERCLOCKWISE )
RightMotor = Motor( Motors['right'],positive_direction = Direction.COUNTERCLOCKWISE )

SortingMotor = Motor( Motors['sort'],positive_direction = Direction.COUNTERCLOCKWISE )

robo = DriveBase( LeftMotor, RightMotor, Wheel_Diameter, Axle_Track )

# Sensors
ColorSensor = ColorSensor( ColorSensor_port )
InfraSensor = UltrasonicSensor( InfraSensor_port )

FrontBtn =  TouchSensor( Buttons['front'] )


##--##--##--## GAME LOOP ##--##--##--##
Ev3.speaker.beep()

turn_count = 0

while RUN:

    # stop the program detection
    if FrontBtn.pressed():
        robo.stop()
        Ev3.speaker.beep('collision with an object')

    # Following wall with infrared sensor
    dist = InfraSensor.distance()
    error = WallDistance - dist
    print(error*koeficient)

    robo.drive(DriveSpeed, error * koeficient)

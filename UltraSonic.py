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
RUN = True

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


##--##--##--## CHECKING THE COLORS ##--##--## 
## TODO: create the ability to configure the colors - right now there is a problem with orange

def color(inputColor):
    if inputColor = Color.BLUE:
        pass # TODO: move the motor right way
    else if inputColor = Color.RED:
        pass # TODO: move the motor right way
    else if inputColor = Color.GREEN:
        pass # TODO: move the motor right way



##--##--##--## CODE CONSTANTS ##--##--##--##
DriveSpeed = 400 # in milemetrs per second

WallDistance = 100 # in % from the sensors maximum
        # TODO: the distances will differ in value based on the drive line we are in
koeficient = -5 # TODO: find the right value

DistanceAvrg = WallDistance
ValuesInAvrg = 10



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

#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

##--##--##--## ROBO CONSTANTS ##--##--## 
from RoboConstants.py import ( Motors, Buttons, ColorSensor_port,
                                Wheel_Diameter, Axle_Track )
RUN = True

##--##--##--## ROBO SET UP ##--##--## 
Ev3 = EV3Brick()

# Motors
LeftMotor = Motor( Motors['left'],positive_direction = Direction.COUNTERCLOCKWISE )
RightMotor = Motor( Motors['right'],positive_direction = Direction.COUNTERCLOCKWISE )

SortingMotor = Motor( Motors['sort'],positive_direction = Direction.COUNTERCLOCKWISE )

robot = DriveBase( LeftMotor, RightMotor, Wheel_Diameter, Axle_Track )

# Sensors
ColorSensor = ColorSensor( ColorSensor_port )

FrontBtn =  TouchSensor( Buttons['front'] )

print( ColorSensor.rgb() )

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

##--##--##--## GAME LOOP ##--##--##--##

turn_count = 0

while RUN:
    robot.drive(DriveSpeed,0)

    # # color detection
    # colorDetected = ColorSensor.color()
    # if colorDetected != None:
    #     color(colorDetected)

    # collision detection
    if FrontBtn.pressed():
        robot.stop()
        robot.turn(90)
        turn_count += 1

        # break the program
        if turn_count == 5:
            break
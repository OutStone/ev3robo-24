#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from color_check import color


##--##--##--## CONSTANTS ##--##
Motors = {
    'left' : 'D',
    'right' : 'A',
    'sort' : '' # TODO: right value (port)
}
Buttons = {
    'front' : 'S1'
}
ColorSensor_port = 'S2'

Wheel_Diameter = 0 # TODO: right value
Axle_Track = 0 # TODO: right value
RUN = True

##--##--##--## SETTING UP THE ROBOT ##--##
Ev3 = EV3Brick()

# Motors
LeftMotor = Motor( Motors['left'],positive_direction = Direction.CLOCKWISE )
RightMotor = Motor( Motors['right'],positive_direction = Direction.COUNTERCLOCKWISE )

SortingMotor = Motor( Motors['sort'],positive_direction = Direction.COUNTERCLOCKWISE )

DriveBase = DriveBase( LeftMotor, RightMotor, Wheel_Diameter, Axle_Track )

# Sensors
ColorSensor = ColorSensor( ColorSensor_port )

FrontBtn =  TouchSensor( Buttons['front'] )


##--##--##--## CHECKING THE COLORS ##--##
## TODO: create the ability to configure the colors - right now there is a problem with orange

def color(inputColor):
    if inputColor = Color.BLUE:
        pass # TODO: move the motor right way
    else if inputColor = Color.RED:
        pass # TODO: move the motor right way
    else if inputColor = Color.GREEN:
        pass # TODO: move the motor right way


##--##--##--## GAME LOOP ##--##
ev3.speaker.beep()

turn_count = 0

while RUN:
    DriveBase.drive()

    # color detection
    colorDetected = ColorSensor.color()
    if colorDetected != None:
        color(colorDetected)

    # collision detection
    if FrontBtn.pressed():
        DriveBase.stop()
        ev3.speaker.say('collision with an object')
        DriveBase.turn(90) # I hope that the code will wait for the robot to turn, otherwise we have a problem
        turn_count += 1

        # break the program
        if turn_count == 2:
            break
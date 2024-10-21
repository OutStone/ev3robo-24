#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# constants
Motors = {
    'left' : '',
    'right' : ''
}
Buttons = {
    'front' : ''
}
Wheel_Diameter = 0 # TODO: right value
Axle_Track = 0 # TODO: right value
RUN = True

# set up the robot
Ev3 = EV3Brick()

LeftMotor = Motor(Motors['left'],positive_direction = Direction.CLOCKWISE)
RightMotor = Motor(Motors['right'],positive_direction = Direction.COUNTERCLOCKWISE)

DriveBase = DriveBase(LeftMotor, RightMotor, Wheel_Diameter, Axle_Track)

FrontBtn =  TouchSensor(Buttons['front'])

# Write your program here.
ev3.speaker.beep()

while run:
    DriveBase.drive()

    if FrontBtn.pressed():
        DriveBase.stop()
        ev3.speaker.say('collision with an object')
        break
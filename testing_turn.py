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

MainMotor = Motor( RC.Motors['main'],positive_direction = Direction.CLOCKWISE )
btn = TouchSensor(RC.Buttons['1'])
Ev3 = EV3Brick()

waiting = input('press to start:')

while True:
    MainMotor.run(180)
    if btn.pressed():
        MainMotor.hold()
        Ev3.speaker.beep()
        wait(1500)

        while btn.pressed():
            MainMotor.run(180)
            
        Ev3.speaker.beep()


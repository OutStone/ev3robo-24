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
ArmMotor = Motor( RC.Motors['arm'],positive_direction = Direction.COUNTERCLOCKWISE )
btn = TouchSensor(RC.Buttons['1'])
Ev3 = EV3Brick()

waiting = input('press to start:')

def move_arm(degs):
    ArmMotor.run_target(180, degs, then=Stop.HOLD, wait=True)
    Ev3.speaker.beep()
    wait(1000)
    ArmMotor.run_target(180, -degs, then=Stop.HOLD, wait=True)
        


while True:
    MainMotor.run(180)

    if btn.pressed():
        MainMotor.hold()
        Ev3.speaker.beep()
        wait(1500)

        move_arm(700)

        while btn.pressed():
            MainMotor.run(180)
            
        Ev3.speaker.beep()


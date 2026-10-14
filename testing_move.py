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
Ev3 = EV3Brick()

# MainMotor.run_target(180, 2000, then=Stop.HOLD, wait=True)
Ev3.speaker.beep()

MainMotor.run_target(45, -45, then=Stop.HOLD, wait=True)
Ev3.speaker.beep()
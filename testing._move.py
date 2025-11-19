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

DriveMotor = Motor( RC.Motors['drive'],positive_direction = Direction.CLOCKWISE )
Ev3 = EV3Brick()

DriveMotor.run(800)
wait(3000)
Ev3.speaker.beep()
DriveMotor.stop()

DriveMotor.run(-800)
wait(3000)
Ev3.speaker.beep()
DriveMotor.stop()
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

ArmMotor = Motor( RC.Motors['arm'],positive_direction = Direction.COUNTERCLOCKWISE )
Ev3 = EV3Brick()

ArmMotor.run(1000)
wait(3000)
Ev3.speaker.beep()
ArmMotor.stop()

wait(10)
ArmMotor.run(-1300)
wait(3000)
Ev3.speaker.beep()
ArmMotor.stop()
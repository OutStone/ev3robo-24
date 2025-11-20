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

##--##--##--## CODE CONSTANTS ##--##--##--##
import CodeCostants as CC

ArmMotor = Motor( RC.Motors['arm'],positive_direction = Direction.COUNTERCLOCKWISE )
Ev3 = EV3Brick()

# ArmMotor.run_time(800,1000)
ArmMotor.run_target(800,1.1*CC.way_in_degs)
# wait(3000)
Ev3.speaker.beep()
# ArmMotor.stop()

# wait(30)
ArmMotor.run_target(800,-0.7*CC.way_in_degs)
# wait(3000)
Ev3.speaker.beep()
# ArmMotor.stop()
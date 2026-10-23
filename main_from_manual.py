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

##--##--##--## CODE CONSTANTS ##--##--##--##
import constants_code as CC


## robo setup
MainMotor = Motor( RC.Motors['main'],positive_direction = Direction.CLOCKWISE )
ArmMotor = Motor( RC.Motors['arm'],positive_direction = Direction.CLOCKWISE )

btn = TouchSensor(RC.Buttons['1'])
Ev3 = EV3Brick()

# just to be sure - however it is most likely redundant
ArmMotor.reset_angle(0)
MainMotor.reset_angle(0)


## variables setup
hodinky = StopWatch()
hodinky.reset()

safety_delay = CC.safety_delay
v_main = CC.Speeds['main']
v_arm  = CC.Speeds['arm' ]


# functions for robo-movement
def _arm(target):
    ArmMotor.run_target(v_arm, target)

def _rotate(target):
    MainMotor.run_target(v_main,target)

angles = CC.angles

hodinky.resume()
for i in angles:
    Ev3.speaker.beep()
    if i[1] == 'Arm':
        _arm(i[0])
    else:
        _rotate(i[0])

    wait(safety_delay)


Ev3.speaker.beep()
hodinky.pause()
t = hodinky.time()

print("End\n time to spare: "+str(90-t/1000)
       + '\n avrg time per piece: '+ str(round(t/(1000*8),2)))
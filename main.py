# 3dilek - objet z venci a tim otocit, pak nabrat do pravy  a pritahnout
# 4dilek - drcnout do nej cestou k 5. a pak ho dotocit a pritahnout az po ulozeni 5.

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
ArmMotor.reset_angle(CC.Arm_start)

btn = TouchSensor(RC.Buttons['1'])
Ev3 = EV3Brick()


## variables setup
hodinky = StopWatch()
hodinky.reset()

v_main = CC.Speeds['main']
v_arm  = CC.Speeds['arm' ]


# functions for robo-movement
def _90deg(angle):
    MainMotor.run_angle(v_main,angle)

def _arm(target):
    ArmMotor.run_target(v_arm, target)

def _rotate(target):
    MainMotor.run_target(v_main,target)


i = 1
while i :
    if i == CC.EndRun_at:
        break

    hodinky.resume()
    _rotate(CC.Deg_vals[i])

    if CC.Turn_piece[i]:
        _90deg(CC.Turn_piece[i])

    _arm(CC.Arm_in[i])

    # tedka je pritahlej - nebude zde potreba nejaky dotrimovani?? - kdyztak pridat podminku
    
    # nejakej edge case pro to otaceni dilku o 180°

    _arm(CC.Arm_out[i])

    hodinky.pause()
    t = hodinky.time()
    
    Ev3.speaker.beep()
    waiting = input('T='+str(t/1000)+'; press to continue:')

print("End\n time to spare: "+str(90-t/1000)
       + '\n avrg time per piece: '+ str(round(t/(1000*i),2)))
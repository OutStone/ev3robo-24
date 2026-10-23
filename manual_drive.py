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
Arm_times = []
Rotor_times = []
last_time = 0

angles = []


v_main = CC.Speeds['main']
v_arm  = CC.Speeds['arm' ]


# begging_angle = int(input('angle on which the arm extender is starting:'))
# ArmMotor.reset_angle(begging_angle)

while True:
    
    Ev3.speaker.beep()

    d = input('(ws - ad - x):')
    if d.lower() == "x":
        break

    k = 1
    if d in ['s','d']:
        k = -1

    if d in ['w','s']:      
        hodinky.resume()
        ArmMotor.run(v_arm * k)
        stop = input('brake:')
        ArmMotor.hold()
        hodinky.pause()
        t = hodinky.time()
        
        Ev3.speaker.beep()
        
        i = len(angles)
        Arm_times.append([ t-last_time,i ])
        angles.append([ ArmMotor.angle(), 'Arm' ])

        print('                    angle: '+ str(round(angles[-1][0]*2,-2)/2) + '; T= ' + str(round(t,-2)) +'; dT= ' +  str(round(Arm_times[-1][0], -2)))
        last_time = t
    elif d in ['a','d']:  
        
        hodinky.resume()
        MainMotor.run(v_main * k)
        
        stop = input('brake:')

        MainMotor.hold()
        hodinky.pause()
        t = hodinky.time()

        Ev3.speaker.beep()
        

        i = len(angles)
        Rotor_times.append([ t-last_time,i ])
        angles.append([ MainMotor.angle(), 'Main' ])

        print('                    angle: '+ str(round(angles[-1][0]*2,-2)/2) + '; T= ' + str(round(t,-2)) +'; dT: ' + str(round(Rotor_times[-1][0], -2)))
        last_time = t


print("End\n time to spare: "+str(90-t/1000),
       '\nangles=',angles,
       '\nRotor_times=',Rotor_times,
       '\nArm_times=',Arm_times)
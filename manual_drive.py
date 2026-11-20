#!/usr/bin/env pybricks-micropython
# pridat revert (all/n tahu zpatky)
import os # for clearing the console
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
Rotor = Motor( RC.Motors['rotor'],positive_direction = Direction.CLOCKWISE )

Arm1 = Motor( RC.Motors['1'],positive_direction = Direction.CLOCKWISE )
Arm2 = Motor( RC.Motors['2'],positive_direction = Direction.CLOCKWISE )


Motors = [  [Rotor],
            [Arm1, Arm2]
]

# Motors = [MainMotor,ArmMotor]

Ev3 = EV3Brick()


## variables setup
hodinky = StopWatch()
hodinky.reset()



Times = [[],[]]
time_last = 0

angles = []

v = {
    "quick" : [CC.Quick['rotor'],CC.Quick['arm']],
    "slow" : [CC.Slow['rotor'],CC.Slow['arm']]
}


# begging_angle = int(input('angle on which the arm extender is starting:'))
# ArmMotor.reset_angle(begging_angle)

stop = ''
while True:
    wait(CC.safety_delay)
    Ev3.speaker.beep()
    # input categorisation
    if True:
        if not stop.lower() in ['w','s','a','d']:
                d = input('(ws - ad - x):')
        else:
            d = stop
            print('going straight to new move')
        
        if d.lower() == "x":
            break
        
        if d.lower() == "reset":
            index = []
            Times = [[],[]]
            os.system("cls")
            print("     reset completed - list of moves is now empty")
            continue
        
        if d.lower() == 't':
            a_t = 0
            for time in Times[1]:
                a_t += time[0]
            print("     T:",time_last, "\n     a_t:",a_t,"\n     r_x",time_last-a_t,"\n     remain:", 90*1000 - time_last)

        # sorting speed boost, motor and the rotation direction
        if True:
            speed_type = 'quick'
            if d.lower() != d:
                speed_type = 'slow'
            # Reverse
            dir = 1
            if d.lower() in ['s','d']:
                dir = -1

            i = 0
            if d.lower() in ['s','w']:
                i = 1
    
    # movement
    if d.lower() in ['w','s','a','d']:
        hodinky.resume()
        
        for m in Motors[i]:
            m.run(v[speed_type][i] * dir)
        
        stop = input('brake or new cmd:')
        
        for m in Motors[i]:
            m.hold()
        
        hodinky.pause()

        t = hodinky.time()
        Ev3.speaker.beep()

        
        # data management
        index = len(angles)
        Times[i].append([
                t-time_last,
                index
        ])
        angles.append([
                Motors[i][0].angle(),
                i,
                speed_type
        ])
        
        print('           angle: '+ str(round(angles[-1][0]*2,-2)/2) + '; T= ' + str(round(t,-2)) +'; dT= ' +  str(round(Times[i][-1][0], -2)))
        if i == 1:
            print('           delta arm:', Motors[1][0].angle() - Motors[1][1].angle() )
        time_last = t
    

print("End\n time to spare: "+str(90-t/1000),
       '\nangles=',angles,
       '\nRotor_times=',Times[0],
       '\nArm_times=',Times[1],
       '\n delta arm=', Motors[1][0].angle() - Motors[1][1].angle())
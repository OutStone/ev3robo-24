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
Arm_times = []
Rotor_times = []
last_time = 0

angles = []


v_main = CC.Speeds['main']
v_arm  = CC.Speeds['arm' ]


#TODO: netucha jak udelat zacatek - na kolika stupnich bude robot zacinat? ma to cislo dostat inputem nebo tam dojet?
begging_angle = int(input('angle on which the arm extender is starting:'))
ArmMotor.reset_angle(begging_angle)

while True:
    typ = input('motor? (empty = extending, "stop" = break cycle):')
    if typ.lower() == "stop":
        break

    direct = input('direction? (empty = counterclock):')

    if direct != "":
        k = -1

    if typ == "":
        
        hodinky.resume()
        while not btn.pressed():
            ArmMotor.run(v_arm * k)
        ArmMotor.hold()
        hodinky.pause()
        t = hodinky.time()
        
        Ev3.speaker.beep()
        
        i = len(angles)
        Arm_times.append([ t-last_time,i ])
        angles.append([ ArmMotor.angle(), 'Arm' ])

        print('angle: '+ str(angles[-1]) +' a cas: ' + str(Arm_times[-1]))
        last_time = t

    else:
        
        hodinky.resume()
        while not btn.pressed():
            MainMotor.run(v_arm * k)
        MainMotor.hold()
        hodinky.pause()
        t = hodinky.time()

        Ev3.speaker.beep()
        

        i = len(angles)
        Rotor_times.append([ t-last_time,i ])
        angles.append([ MainMotor.angle(), 'Main' ])

        print('angle: '+ str(angles[-1]) +' a cas: ' + str(Rotor_times[-1]))
        last_time = t



print("End\n time to spare: "+str(90-t/1000),
       '\n angles=',angles,
       '\n Rotor_times=',Rotor_times,
       '\n Arm_times=',Arm_times)
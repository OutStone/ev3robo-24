#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Direction, Button
from pybricks.tools import wait, StopWatch, DataLog

##--##--##--## ROBO CONSTANTS ##--##--## 
import constants_robo as RC

##--##--##--## CODE CONSTANTS ##--##--##--##
import constants_code as CC


## robo setup
if True:
    Rotor = Motor( RC.Motors['rotor'],positive_direction = Direction.CLOCKWISE )

    Arm1 = Motor( RC.Motors['1'],positive_direction = Direction.CLOCKWISE )
    Arm2 = Motor( RC.Motors['2'],positive_direction = Direction.CLOCKWISE )


    Motors = [  [Rotor],
                [Arm1, Arm2]
    ]

    Btn_l = 1#TouchSensor(RC.Buttons['l'])
    Btn_r = 2#TouchSensor(RC.Buttons['r'])

    Btns = [ 
        Btn_l,
        Btn_r
    ]

    Ev3 = EV3Brick()

## variables setup
if True:
    hodinky = StopWatch()
    hodinky.reset()

    v = CC.v
    
    Move_log = CC.Move_log
    record_index = 0


def reset():
    hodinky.reset()
    Motors[0][0].reset_angle(0)
    Motors[1][0].reset_angle(0)
    Motors[1][1].reset_angle(0)

## movement funcs
def checkpoints(n):
    global hodinky, Motors, v
    dir = 1 if n < 0 else -1
    n = abs(n)
    reached = [n, n] 
    now_pressed = [False, False] 

    # robo starts with already pressed btn -> target number is highered (this btn does not count)
    for i in [0,1]:
        if Btns[i].pressed():
            reached[i] += 1
    
    Motors[1][0].run(v["quick"][1] * dir)
    Motors[1][1].run(v["quick"][1] * dir)
            
    while reached[0] + reached[1] != 0:
        for i in [0,1]:
            if reached[i] == 0:
                continue
                
            if Btns[i].pressed():
                if not now_pressed[i]:
                    now_pressed[i] = True

                    reached[i] -= 1
                    if reached[i] == 0:
                        Motors[1][i].hold()
            else:
                if now_pressed[i]: 
                    now_pressed[i] = False
        
        wait(CC.button_delay)

def recorded_angle(cmd):
    global hodinky, Motors, v
    i = cmd[2]

    if len(Motors[ i ]) > 1:
        Motors[i][0].run_target(
                    v[ cmd[3] ][ cmd[2] ], # speed - first coord carries boost values
                    cmd[1],
                    wait=False
        )
    Motors[i][ -1 ].run_target(         # running the first motor from the end, there are either two or just one motor.  for two it now runs the secodn one (the first one is already running asynchonously) 
                    v[ cmd[3] ][ cmd[2] ], # speed - first coord carries boost values
                    cmd[1]
    )

def _2D(r,a):
    global Motors, v
    
    Motors[0][0].run_target(
                v['fast'][0],
                r,
                 wait=False
    )
    Motors[1][0].run_target(
                v['fast'][1],
                a,
                wait=False
        )
    Motors[1][1].run_target(
                v['fast'][1],
                a
    )
    while abs(Motors[0][0].speed()) > 10: # TODO: nechci tady pridat kontrolu i toho druhyho z ramena?
        wait(CC._2d_delay)

def single(t,i):
    alpha = Motors[1][i].angle()
    
    Motors[1][i].reset_angle(alpha - t)
    Motors[1][i].run_target(
                v[ 'quick' ][ 1 ], # speed - first coord carries boost values
                alpha,
    )

def manual(i, dir):
    global hodinky, Motors, v, Ev3
            
    for m in Motors[i]:
        m.run(v['slow'][i] * dir)

    while not Button.CENTER in Ev3.buttons.pressed():
        wait(10)

    for m in Motors[i]:
        m.hold()

    while Button.CENTER in Ev3.buttons.pressed():
        wait(10)

    wait(50)
    Ev3.speaker.beep()
    return




Ev3.speaker.beep()
while not Button.CENTER in Ev3.buttons.pressed():
    if len(Ev3.buttons.pressed()) > 0:
        b = Ev3.buttons.pressed()[0]

        dir = 1
        if b in [Button.DOWN,Button.RIGHT]:
            dir = -1
        i = 0
        if b in [Button.DOWN,Button.UP]:
            i = 1

        manual(i,dir)

print('out of setup')
hodinky.resume()
reset()

for cmd in Move_log:
    Ev3.speaker.beep()
    print('cycling')
    

    if cmd[0] == 'A':
        recorded_angle(cmd)
    elif cmd[0] == 'P':
        checkpoints(cmd[1])
    elif cmd[0] == 'D':
        _2D(cmd[1],cmd[2])
    elif cmd[0] == 'S':
        single(cmd[1],cmd[2])   

    wait(CC.safety_delay) #TODO: maybe shorten?

# End data
Ev3.speaker.beep()
hodinky.pause()
t = hodinky.time()

print("End",
      '\n time to spare: '+str(90-t/1000),
      '\n avrg time per piece: '+ str(round(t/(1000*8),2)),
       '\n sum of all waiting: ' + str( len(Move_log) * CC.safety_delay)
)
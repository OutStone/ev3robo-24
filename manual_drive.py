#!/usr/bin/env pybricks-micropython
# pridat revert (all/n tahu zpatky) - asi na to kaslu
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
if True:
    Rotor = Motor( RC.Motors['rotor'],positive_direction = Direction.CLOCKWISE )

    Arm1 = Motor( RC.Motors['1'],positive_direction = Direction.CLOCKWISE )
    Arm2 = Motor( RC.Motors['2'],positive_direction = Direction.CLOCKWISE )


    Motors = [  [Rotor],
                [Arm1, Arm2]
    ]

    Btn_l = TouchSensor(RC.Buttons['l'])
    Btn_r = TouchSensor(RC.Buttons['r'])

    Btns = [ 
        Btn_l,
        Btn_r
    ]

    Ev3 = EV3Brick()

## variables setup
if True:
    hodinky = StopWatch()
    hodinky.reset()


    Time_log = [[],[]]
    t = 0
    time_last = 0

    Move_log = []

    v = {
        "quick" : [CC.Quick['rotor'],CC.Quick['arm']],
        "slow" : [CC.Slow['rotor'],CC.Slow['arm']]
    }
    
    Record_log = CC.Move_log
    record_index = 0

# helping funcs
def move_info(i):
    global time_last,t,Motors,Move_log,Time_log
    gap = '           '
    print(gap + 'angle: '+ str(round(Move_log[-1][1]*2,-2)/2))
    print(gap + '   T=  '+ str(round(t,-2)) +'; dT= ' +  str(round(Time_log[ i ][0], -2)))
    if i == 1:
        print(gap + 'delta arm:', Motors[1][0].angle() - Motors[1][1].angle() )
    time_last = t

def reset():
    index = []
    Move_log = []
    Time_log = [[],[]]
    hodinky.reset()
    time_last = 0
    record_index = 0

    Motors[0][0].reset_angle(0)
    Motors[1][0].reset_angle(0)
    Motors[1][1].reset_angle(0)

    cls()
    print("     reset completed - list of moves is now empty")

def log():
    print("time to spare: "+str(90-t/1000),
        '\nMove_log=',Move_log,
        '\nRotor_times=',Time_log[0],
        '\nArm_times=',Time_log[1],
        '\n delta arm=', Motors[1][0].angle() - Motors[1][1].angle())

def cls():
    print("\x1b[2J\x1b[H", end="")

# movement funcs
def manual(i,speed_type, dir):
    global hodinky, Motors, v, Ev3
    global Time_log, Move_log, time_last, t, stop
    hodinky.resume()
            
    for m in Motors[i]:
        m.run(v[speed_type][i] * dir)

    # waiting for stop signal
    stop = input('brake or new cmd:')
    
    for m in Motors[i]:
        m.hold()
    
    hodinky.pause()

    t = hodinky.time()
    Ev3.speaker.beep()

    
    # DATA management
    index = len(Move_log)
    Time_log[i].append([
            t-time_last,
            index
    ])
    Move_log.append([
            'A',
            Motors[i][0].angle(),
            i,
            speed_type
    ])

    move_info(i)
    time_last = t


def checkpoints(n):
    global hodinky, Motors, v
    dir = 1 if n < 0 else -1
    n = abs(n)
    reached = [n, n] 
    now_pressed = [False, False] 
    
    hodinky.resume()
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
    hodinky.pause()

# Following STORED COMMANDS
def recorded_angle(cmd):
    global hodinky, Motors, v
    i = cmd[2]

    hodinky.resume()
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
    hodinky.pause()


def from_record(index):
    global hodinky, Ev3, Motors, Time_log, Move_log, time_last, t

    if index >= len(Record_log):
        print('Whole Record was replayed')
        print(' - no command to do')
        return
    cmd = Record_log[index]

    # the MOVEMENT
    typ = cmd[0] 
    if typ == 'A':
        recorded_angle(cmd)
    if typ == 'P':
        checkpoints(cmd[1])

    # DATA management
    if True:
        t = hodinky.time()
        Time_log[cmd[2]].append([
                t-time_last,
                len(Move_log)
        ])
        Move_log.append([
                cmd[0],
                cmd[1],
                cmd[2],
                cmd[3]
        ])
    move_info(cmd[2])
    time_last = t

# other movement
def restart():
        # arm half way home
        if True:
            Motors[1][0].run_target(
                        v[ "quick" ][ 1 ], # speed - first coord carries boost values
                        -570,
                        wait = False
            )
            Motors[1][ 1 ].run_target(         # running the first motor from the end, there are either two or just one motor.  for two it now runs the secodn one (the first one is already running asynchonously) 
                            v[ "quick" ][ 1 ], # speed - first coord carries boost values
                            -570
            )

        # rotor home
        Motors[0][ 0 ].run_target(         # running the first motor from the end, there are either two or just one motor.  for two it now runs the secodn one (the first one is already running asynchonously) 
                        v[ "quick" ][ 0 ], # speed - first coord carries boost values
                        0
        )

        # arm home
        if True:
            Motors[1][ 0 ].run_target(         # running the first motor from the end, there are either two or just one motor.  for two it now runs the secodn one (the first one is already running asynchonously) 
                            v[ "quick" ][ 0 ], # speed - first coord carries boost values
                            0,
                            wait = False
            )
            Motors[1][ 1 ].run_target(         # running the first motor from the end, there are either two or just one motor.  for two it now runs the secodn one (the first one is already running asynchonously) 
                            v[ "quick" ][ 0 ], # speed - first coord carries boost values
                            0
            )

stop = ''
while True:
    wait(CC.safety_delay)
    Ev3.speaker.beep()
    
    # INPUT
    if True:
        if not len(stop):
                d = input('(ws - ad - x):')
        else:
            d = stop
            print('going straight to new move')

    # NO INPUT
    if d == '': continue

    # END of CYCLE
    if d.lower() == "x":
        break

    # RESET of MOVEMENT RECORDING
    if d.lower() == "reset": reset()
        
    # LOG of TIME
    if d.lower() == 't':
        a_t = 0
        for time in Time_log[1]:
            a_t += time[0]

        print("     T:",time_last,
            "\n     a_t:",a_t,
            "\n     r_x",time_last-a_t,
            "\n     remain:", 90*1000 - time_last)
        continue
    
    # REWRITE current POS
    if d.lower() == 'edit':
        x = int(input("arm:"))
        y = int(input("rotor:"))

        Motors[0][0].reset_angle(y)
        Motors[1][0].reset_angle(x)
        Motors[1][1].reset_angle(x)
    
    if d.lower() == 'log':
        cls()
        log()
        a = input('press to continue (console will be cleared)')
        cls()
        continue

    if d.lower() == "restart": restart()

    # sorting speed boost, motor and the rotation direction
    if True:
            speed_type = 'quick'
            if d.lower() != d:
                speed_type = 'slow'
            # Reverse
            dir = 1
            if d[0].lower() in ['s','d','e']:
                dir = -1

            i = 0
            if d.lower() in ['s','w']:
                i = 1

    if d[0].lower() in ['e','q']:
        n = int(d[2:]) * dir # dvojtecka kdyby jich bylo vic jak 10
        checkpoints(n)
        
        t = hodinky.time()
        Time_log[1].append([
                t-time_last,
                len(Move_log)
        ])
        Move_log.append([
                'P',
                n,
                1,
                "quick"
        ])
        move_info(1)
        time_last = t


    # MOVEMENT - no mechanical stops
    if d.lower() in ['w','s','a','d']:  manual(i,speed_type,dir)

    
    # - copying old moves
    if d[0].lower() == 'l':
        ask_questions = d[0].lower() == d[0] # if "l" is lower case, then it asks questions

        l = d.split()
        if len(l) >= 1:
            n = int(l[1])

            if len(l) > 1:
                record_index = int(l[2])
                
            if n < 0:
                n = len(Record_log) - record_index
        else:
            n = 1


        counter = 0
        while True:
            from_record(record_index);   record_index += 1

            counter += 1
            if counter < n:
                if ask_questions:
                    stop = input('press for next move (key = end):')
                    if stop != '':
                        break
            else:
                break

if d.lower() == d:
    restart()
cls()
print("End")
log()
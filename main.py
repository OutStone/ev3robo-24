#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

##--##--##--## DATA LOG ##--##--## 
log = ""

##--##--##--## ROBO CONSTANTS ##--##--## 
import RoboConstants as RC

##--##--##--## CODE CONSTANTS ##--##--##--##
import CodeCostants as CC

##--##--##--## ROBO SET UP ##--##--##
if True:
    Ev3 = EV3Brick()

    # Motors
    ThirdMotor = Motor( RC.Motors['third'],positive_direction = Direction.COUNTERCLOCKWISE )
    LeftMotor = Motor( RC.Motors['left'],positive_direction = Direction.CLOCKWISE )
    RightMotor = Motor( RC.Motors['right'],positive_direction = Direction.CLOCKWISE )

    robot = DriveBase( LeftMotor, RightMotor, RC.Wheel_Diameter, RC.Axle_Track )
    robot.settings(straight_speed=2*CC.DriveSpeed)

    # Sensors
    FrontBtn = TouchSensor( RC.Buttons['front'] )
    SideBtn = TouchSensor( RC.Buttons['side'] )

    ColorSensor = ColorSensor( RC.ColorSensor_port )

    # Gyro = GyroSensor( RC.Gyro_port )
    # InfraSensor = InfraredSensor( RC.InfraSensor_port )
    UlraSensor = UltrasonicSensor( RC.UlraSensor_port )

##--##--##--## Driving Funcions ##--##--##--##
def ServoTurn(fraction_of_circle, speed): # in deg/s & deg
    robot.stop() # TODO: potentionaly too redundant -> remove after a check of functions usage in code

    Angle_left  = (RC.Axle_Track/RC.Wheel_Diameter) * fraction_of_circle * -1 * 360
    Angle_right = (RC.Axle_Track/RC.Wheel_Diameter) * fraction_of_circle      * 360

    RightMotor.run_angle( speed, Angle_right,wait=False )
    LeftMotor.run_angle(  speed, Angle_left )
    print("konec zataceni")

    robot.stop()

def Stop_Dist(target):
    global log
    dist = UlraSensor.distance() + CC.DistanceSensor_Offset['backwards']
    log += str(dist) + "     "
    if dist >= CC.UltraSensorMax:
        print("\033[92m Ultra reporting max value \033[00m")
        return True
    elif dist >= target:
        return True
    
    return False

def Follow_Ultra(target):
        global previous_error
        dist = UlraSensor.distance()

        error = target - dist

        derivative = error - previous_error

        correction = CC.proportial_gain * error + CC.derivative_gain * derivative
        previous_error = error

        left_speed = CC.RotationSpeed + correction
        right_speed = CC.RotationSpeed - correction

        RightMotor.run(left_speed)
        LeftMotor.run(right_speed)

def Follow_Mechanical():
    global Lost_the_wall
    if SideBtn.pressed(): # True -> we are directly next to wall
        robot.drive(CC.DriveSpeed * 3.14 * RC.Wheel_Diameter/360, CC.FollowAngle['ok'])
        Lost_the_wall = False
    else: # time to search where the lost wall is
        if not Lost_the_wall:
            Drive_Clock.reset()
            Drive_Clock.resume()
            Lost_the_wall = True
            robot.drive(CC.DriveSpeed * 3.14 * RC.Wheel_Diameter/360, CC.FollowAngle['btn-off'])
        elif Drive_Clock.time() > 1000:
            robot.drive(CC.DriveSpeed * 3.14 * RC.Wheel_Diameter/360, 0)

def Follow_Color():
    global log
    Color_now = ColorSensor.color()
    log += str(Color_now) + "     "
    if Color_now == Color.BLACK: # now it wants to find white => turning left
        RightMotor.run(CC.RotationSpeed*(1-CC.black_koef))
        LeftMotor.run(CC.RotationSpeed *(1+CC.black_koef))
        
    elif Color_now == Color.WHITE: # now it wants to find black => turning right
        RightMotor.run(CC.RotationSpeed*(1+CC.white_koef))
        LeftMotor.run(CC.RotationSpeed *(1-CC.white_koef))

    else: # this is the same as for white, but it should not happen so better make a note in game log
        log += "\033[93m LACK OF LIGHT:\033[00m " # in Yellow
        RightMotor.run(CC.RotationSpeed*(1+CC.white_koef))
        LeftMotor.run(CC.RotationSpeed *(1-CC.white_koef))
    log += str(Color_now) + "     "

##--##--##--## working with tetris tiles ##--##--## 
def Move_Gate(direct,wait_for_it=True):
    # this func does both open & close the gate
    if direct.lower() == "open":
        flag = 1
    elif direct.lower() == "close":
        flag = -1
    else:
        print("\033[91m incorrect direction input to gate moving func '{}'\033[00m ".format(direct))

    ThirdMotor.run_angle(
        CC.GateSpeed,
        CC.GateAngle * flag,
        then=Stop.HOLD,
        wait=wait_for_it
    )
    
##--##--##--## GAME LOOP ##--##--##--##
if True: # set up of variables
    # driving
    End_of_stage = False # substitutes for a button press -> iniciates a robot turn
    Lost_the_wall = False # zero.. everything ok;  1 ... a problem -> trying to drive back to target

    # ultrasonic wall follow
    previous_error = 0

    Drive_Clock = StopWatch() # measuring robot turn angle in mechanical follow
    Drive_Clock.pause()
    Drive_Clock.reset()

    Game_Clock = StopWatch() # for game timing
    Game_Clock.pause()
    Game_Clock.reset()
        
    Cycle_Clock = StopWatch() # for stable game loops
    Cycle_Clock.pause()
    Cycle_Clock.reset()

Start = False
while True:
    if SideBtn.pressed():
        Start = True
    elif Start:
        # upon releasing the button (may take multiple game cycles) starts the game
        Game_Clock.resume()
        Cycle_Clock.resume()
        break

while True: # game loop
    
    if Game_Clock.time() >= CC.GameLenght:
        # the game time is up => robot should stop
        Ev3.speaker.beep()
        break

    # stop the program detection
    if FrontBtn.pressed() or End_of_stage:
        # reseting driving clock
        Drive_Clock.pause()
        Drive_Clock.reset()

        # reseting variables
        End_of_stage = False
        previous_error = 0
        Lost_the_wall = False

        
        # stoping the robot after movent
        robot.stop()

        
        CC.DrivingStage += 1

        # forced stop
        if CC.DrivingStage == CC.EndRun:
            break


    # driving stage logic
    if  CC.DrivingStage == 0: # closes the storage
        End_of_stage = True
        Move_Gate(CC.StageValues[ CC.DrivingStage ])
    elif CC.DrivingStage == 1: ## color follow  && max distance from wall to reach
        Follow_Color()
        End_of_stage = Stop_Dist(CC.StageValues[ CC.DrivingStage ]) # if I reached the target it returns True => next stage will activite
    elif CC.DrivingStage == 2: # closes the storage
        End_of_stage = True
        Move_Gate(CC.StageValues[ CC.DrivingStage ])
    elif CC.DrivingStage == 3:
        robot.straight(CC.StageValues[ CC.DrivingStage ] + CC.DistanceSensor_Offset[ 'backwards' ])
        End_of_stage = True
    elif CC.DrivingStage == 4:
        ServoTurn(-0.25 , CC.RotationSpeed)
        End_of_stage = True
    elif CC.DrivingStage == 5:
        ServoTurn(0.25 , CC.RotationSpeed)
        End_of_stage = True
    else:
        Ev3.speaker.beep()
        print("\033[92m End\033[00m")
        break
    
    # constant time program cycle
    #TODO: Maybe remove this, 'cause this year we are not gonna follow a will with Ultra-sensor
    if Cycle_Clock.time() < CC.LoopTime: # spare time -> waits
        wait(CC.LoopTime - Cycle_Clock.time())

    else: # not enought time
        pass
        print('\033Err: cycle took to long!\033') # printing in red color
        print(Cycle_Clock.time())
    
    Cycle_Clock.reset()

    # managing the game log
    print(log)
    log = ""
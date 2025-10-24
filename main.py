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

##--##--##--## ROBO SET UP ##--##--##
if True:
    Ev3 = EV3Brick()

    # Motors
    ThirdMotor = Motor( RC.Motors['third'],positive_direction = Direction.COUNTERCLOCKWISE )
    LeftMotor = Motor( RC.Motors['left'],positive_direction = Direction.COUNTERCLOCKWISE )
    RightMotor = Motor( RC.Motors['right'],positive_direction = Direction.COUNTERCLOCKWISE )

    robot = DriveBase( LeftMotor, RightMotor, RC.Wheel_Diameter, RC.Axle_Track )

    # Sensors
    FrontBtn = TouchSensor( RC.Buttons['front'] )
    SideBtn = TouchSensor( RC.Buttons['side'] )

    ColorSensor = ColorSensor( RC.ColorSensor_port )

    # Gyro = GyroSensor( RC.Gyro_port )
    # InfraSensor = InfraredSensor( RC.InfraSensor_port )
    UlraSensor = UltrasonicSensor( RC.UlraSensor_port )

##--##--##--## Driving Funcions ##--##--##--##
def ServoTurn(left, right, speed): # in deg/s & deg
    robot.stop()

    Angle_left = (RC.Axle_Track/(4*RC.Wheel_Diameter)) * left * 180*-1
    Angle_right = (RC.Axle_Track/(4*RC.Wheel_Diameter)) * right * 180

    Speed_left = speed * left
    Speed_right = speed * right

    RightMotor.run_angle( Speed_right, Angle_right,wait=False )
    LeftMotor.run_angle( Speed_left, Angle_left )
    print("konec zataceni")

    robot.stop()

def Follow_Ultra(target):
        global previous_error
        dist = UlraSensor.distance()/10

        print(round(dist, 3))

        error = target - dist

        derivative = error - previous_error

        correction = CC.proportial_gain * error + CC.derivative_gain * derivative
        previous_error = error

        left_speed = CC.DriveSpeed + correction
        right_speed = CC.DriveSpeed - correction

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

##--##--##--## working with tetris tiles ##--##--## 
def Move_gate(direct):
    # this func does both open & close the gate
    if direct.lower() == "open":
        flag = -1
    elif direct.lower() == "close":
        flag = 1
    else:
        print("incorrect direction input to gate moving func")

    ThirdMotor.run_angle(
        CC.GateSpeed,
        CC.GateAngle * flag,
        then=Stop.HOLD,
        wait=True
    )
    
##--##--##--## GAME LOOP ##--##--##--##
if True: # set up of variables
    # driving
    ForcedTurn = False # substitutes for a button press -> iniciates a robot turn
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
    if FrontBtn.pressed():
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
    if FrontBtn.pressed() or ForcedTurn:
        # reseting driving clock
        Drive_Clock.pause()
        Drive_Clock.reset()

        # reseting variables
        ForcedTurn = False
        previous_error = 0
        Lost_the_wall = False

        
        # stoping the robot after ulrasonic wall follow  x  after evrth. else
        if CC.DrivingStage in CC.UltraFollowStages:
            LeftMotor.stop()
            RightMotor.stop()
        else:
            robot.stop()

        
        CC.DrivingStage += 1

        # forced stop
        if CC.DrivingStage == CC.StopAt:
            break
        
        # turning
        Ev3.speaker.beep()
        if CC.DrivingStage in CC.DoNotTurn:
            pass
        elif CC.DrivingStage in CC.ReverseTurns:
            ServoTurn(-2,3,60)
        else:
            ServoTurn(-2,3,-60)

        # specific driving stage things
        if CC.DrivingStage == 4:
            robot.reset()

    # driving stage logic
    if   CC.DrivingStage == 1: ## Sensor follow
        robot.straight(CC.StageValues[ CC.DrivingStage ])
    else:
        break
    
    # constant time program cycle
    if Cycle_Clock.time() < CC.LoopTime: # spare time -> waits
        wait(CC.LoopTime - Cycle_Clock.time())

    else: # not enought time
        print('\033Err: cycle took to long!\033') # printing in red color
        print(Cycle_Clock.time())
    
    Cycle_Clock.reset()
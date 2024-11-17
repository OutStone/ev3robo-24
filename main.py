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
    SortingMotor = Motor( RC.Motors['sort'],positive_direction = Direction.COUNTERCLOCKWISE )
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
def ServoTurn( Speed, Angle ): # in deg/s & deg
    # equation for number of wheel turns ( x )
    # x = (Turning radius/wheel radius) * (turning angle/360 deg)

    reverse_dist = 80 # in mm

    robot.straight(-1*reverse_dist)
    robot.stop()

    Radius_Ratio = RC.Axle_Track/(RC.Wheel_Diameter/2)
    Angle_Fraction = Angle/360

    if Angle > 0: # turning left - left wheel stands
        Right_Angle = Can_Right * (Angle_Fraction * Radius_Ratio) * 360 * CC.TurnErr
        print("zatacim do leva", Right_Angle)

        RightMotor.run_angle( Speed,Right_Angle )
    else: # turning right
        Left_Angle = (Angle_Fraction * Radius_Ratio) * 360 * -1  * CC.TurnErr
        print("zatacim do prava", Left_Angle)
        LeftMotor.run_angle( Speed,Left_Angle  )
    print("konec zataceni")

    robot.stop()

def Follow_Ultra(target):
        global integral, previous_error
        dist = UlraSensor.distance()/10

        print(round(dist, 3))

        error = target - dist

        integral += error
        derivative = error - previous_error

        correction = CC.proportial_gain * error + CC.integral_gain * integral + CC.derivative_gain * derivative
        previous_error = error

        left_speed = CC.DriveSpeed + correction
        right_speed = CC.DriveSpeed - correction

        RightMotor.run(left_speed)
        LeftMotor.run(right_speed)

def Follow_Mechanical():
    global Fixing
    if SideBtn.pressed(): # if True then we are directly next to wall
        robot.drive(CC.DriveSpeed, CC.FollowAngle['ok'])
        Fixing = 0
    else: # if True then we are directly next to wall
        if not Fixing:
            Drive_Clock.reset()
            Drive_Clock.resume()
            Fixing = 1
            robot.drive(CC.DriveSpeed, CC.FollowAngle['btn-off'])
        elif Drive_Clock.time() > 1000:
            robot.drive(CC.DriveSpeed, 0)

##--##--##--## working with colors ##--##--## 
def Sort_Func( DetectedColor, sort ): # sorts the ping pong balls
    global Now_Sorting, Back_Direction
    if int(Sort_Clock.time()) != 0:
       print("we have a problem with Stopwatch not being at zero after a pause and reset, for easier debuging here is the time: ", Sort_Clock.time())
    
    if sort:
        if DetectedColor == Color.RED:
            Sort_Clock.resume()
            Now_Sorting = True
            
            print('red')
            SortingMotor.run_angle(
                CC.SortSpeed,
                CC.SortAngle['red'],
                then=Stop.BRAKE,
                wait=False
            )
            Back_Direction = 'red'

        elif DetectedColor == Color.BLUE:
            Sort_Clock.resume()
            Now_Sorting = True
            
            print('blue')
            
            SortingMotor.run_angle(
                CC.SortSpeed,
                CC.SortAngle['blue'],
                then=Stop.BRAKE,
                wait=False
            )
            Back_Direction = 'blue'
        else:
            #print("ERROR: unknown color: ", DetectedColor) # quite common - TODO: change sth to make it rarer
            Now_Sorting = False
    else:
        Sort_Clock.resume()
        Now_Sorting = True
        
        print('part 2 sort')
        # no need to sort by color - balls are just picked up into the same container to be throwed on oponent's side  
        SortingMotor.run_angle(CC.SortSpeed, CC.SortAngle['red'], then=Stop.BRAKE, wait=False)

##--##--##--## Other func ##--##--##--##
def sign(a): # return a mathematical sign of a given number ( + 0 - )
    a = int(a)
    if a == 0:
        return 0
    elif a > 0:
        return -1
    else:
        return 1

##--##--##--## GAME LOOP ##--##--##--##
if True: # set up of variables
    # driving
    ForcedTurn = False # substitutes for a button press -> iniciates a robot turn
    Fixing = 0 # zero.. everything ok 1 ... a problem - trying to drive back to target

    # ultrasonic wall follow
    previous_error = 0
    integral = 0

    Drive_Clock = StopWatch() # measuring robot turn angle in mechanical follow
    Drive_Clock.pause()
    Drive_Clock.reset()

    # color sorting
    Now_Sorting = False
    Back_Direction = None

    Sort_Clock = StopWatch() # for stopping sorting motor (TODO: test if I can stop based on motor angle)
    Sort_Clock.pause()
    Sort_Clock.reset()

    Game_Clock = StopWatch() # for game timing
        
    Cycle_Clock = StopWatch() # for stable game loops

while True: # game loop

    # color detection
    DetectedColor = ColorSensor.color()

    if DetectedColor != None and not Now_Sorting:
        Sort_Func( DetectedColor, CC.Do_ColorSort )

    if Now_Sorting and int(Sort_Clock.time()) > CC.SortTime:
        if Back_Direction:
            print('changing in time: ', Sort_Clock.time(), ' now going to starting place')
            Sort_Clock.reset()

            SortingMotor.run_angle(
                CC.SortSpeed,
                -1* CC.SortAngle[Back_Direction] + sign(CC.SortAngle[Back_Direction])*5, # the second part makes the motor move on the way back a bit less
                then=Stop.BRAKE,
                wait=False
            )
            Back_Direction = None
        else:
            Sort_Clock.pause()
            print('changing bool "Now_Sorting" in time: ', Sort_Clock.time())
            Sort_Clock.reset()

            Now_Sorting = False

    # stop the program detection
    if FrontBtn.pressed() or ForcedTurn:
        # reseting driving clock
        Drive_Clock.pause()
        Drive_Clock.reset()

        # reseting variables
        previous_error = 0
        integral = 0
        Fixing = 0

        
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
        if CC.DrivingStage in CC.TestingTurn_ProblemArea:
            print('                     problem area')
            robot.straight(-60)
        ServoTurn(400,-90)

        # specific driving stage things
        if CC.DrivingStage == 4:
            robot.reset()
        elif CC.DrivingStage == 5:
            ForcedTurn = False

    # driving stage logic
    if   CC.DrivingStage == 1: ## Sensor follow
        # Following wall with infrared sensor
        Follow_Ultra( CC.StageValues[CC.DrivingStage] )
    elif CC.DrivingStage == 2: ## Mechanical follow
        Follow_Mechanical()
    elif CC.DrivingStage == 3: ## Mechanical follow
        Follow_Mechanical()
    elif CC.DrivingStage == 4: ## Mechanical follow with distnace measurement
        ahead = robot.distance()
        Follow_Mechanical()

        if ahead >= CC.StageValues[4]:
            ForcedTurn = True
    else:
        dist = UlraSensor.distance()
        print('wall distance after last turn: ', dist)
        break

        # making a constant time drive loop 
    
    # constant time program cycle
    if Cycle_Clock.time() < CC.LoopTime: # spare time -> waits
        wait(CC.LoopTime - Cycle_Clock.time())
    else: # not enought time
        print('\033Err: cycle took to long!\033') # printing in red color
        print(Cycle_Clock.time())
    
    Cycle_Clock.reset()
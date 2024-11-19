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
        global integral, previous_error
        dist = UlraSensor.distance()/10

        print(round(dist, 3))

        error = target - dist

        integral += error
        derivative = error - previous_error

        correction = CC.proportial_gain * error + CC.integral_gain * integral + CC.derivative_gain * derivative
        previous_error = error # nice

        left_speed = CC.DriveSpeed + correction
        right_speed = CC.DriveSpeed - correction

        RightMotor.run(left_speed)
        LeftMotor.run(right_speed)

def Follow_Mechanical():
    global Fixing
    if SideBtn.pressed(): # if True then we are directly next to wall
        robot.drive(CC.DriveSpeed * 3.14 * RC.Wheel_Diameter/360, CC.FollowAngle['ok'])
        Fixing = 0
    else: # if True then we are directly next to wall
        if not Fixing:
            Drive_Clock.reset()
            Drive_Clock.resume()
            Fixing = 1
            robot.drive(CC.DriveSpeed * 3.14 * RC.Wheel_Diameter/360, CC.FollowAngle['btn-off'])
        elif Drive_Clock.time() > 1000:
            robot.drive(CC.DriveSpeed * 3.14 * RC.Wheel_Diameter/360, 0)

def Reverse_Follow_Mechanical():
    global Fixing, ForcedTurn
    if not Fixing:
        Drive_Clock.reset()
        Drive_Clock.resume()
        Fixing = 1
        robot.drive(CC.DriveSpeed * 3.14 * RC.Wheel_Diameter/360 * -1, CC.FollowAngle['btn-off']/1.3)
    elif Drive_Clock.time() > 1000 and Drive_Clock.time() < StageValues[6]: # from 1000 to 4000
        robot.drive(CC.DriveSpeed * 3.14 * RC.Wheel_Diameter/360 * -1, 0)
    elif Drive_Clock.time() > StageValues[6]: # from 4000
        robot.stop()
        print('FORCED TURN')
        ForcedTurn = True
##--##--##--## working with colors ##--##--## 
def Sort_Func( DetectedColor, sort ): # sorts the ping pong balls
    global Now_Sorting, Back_Direction
    if sort:
        if DetectedColor == Color.RED:
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
            #print("ERROR: unknown color: ", DetectedColor) # quite common - TODO: OPT change sth to make it rarer
            Now_Sorting = False
    else:
        Now_Sorting = True
        
        print('part 2 sort')
        # no need to sort by color - balls are just picked up into the same container to be throwed on oponent's side  
        SortingMotor.run_angle(CC.SortSpeed, CC.SortAngle['red'], then=Stop.BRAKE, wait=False)

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

    Game_Clock = StopWatch() # for game timing
    Game_Clock.pause()
    Game_Clock.reset()
        
    Cycle_Clock = StopWatch() # for stable game loops
    Cycle_Clock.pause()
    Cycle_Clock.reset()

    Dumping_Clock = StopWatch()
    Dumping_Clock.pause()
    Dumping_Clock.reset()

##--##--##--## Set up of sorting sys ##--##--##--##
SortingMotor.run_until_stalled(CC.SortSpeed, Stop.COAST, 40)
wait(1000)
SortingMotor.run_angle(
    CC.SortSpeed,
    -600,
    then=Stop.BRAKE,
    wait=True
)

Start = False
print('press the button!!')
while True:
    if FrontBtn.pressed():
        Start = True
    elif Start:
        Game_Clock.resume()
        Cycle_Clock.resume()
        break

while True: # game loop
    
    if Game_Clock.time() >= CC.GameLenght:
        Ev3.speaker.beep()
        break

    # color detection
    DetectedColor = ColorSensor.color()
    if DetectedColor != None and not Now_Sorting:
        Sort_Func( DetectedColor, CC.Do_ColorSort )

    if Now_Sorting:
        if Back_Direction:
            if abs(SortingMotor.angle()) >= abs(CC.SortAngle[Back_Direction]):

                SortingMotor.run_angle(
                    CC.SortSpeed,
                    -1* CC.SortAngle[Back_Direction], # the second part makes the motor move on the way back a bit less
                    then=Stop.BRAKE,
                    wait=False
                )
                print('changing sort direction')

                Back_Direction = None
        elif not Back_Direction:
            if abs(SortingMotor.angle()) <= 5:
                print('sorting finished')
                Now_Sorting = False

    # stop the program detection
    if FrontBtn.pressed() or ForcedTurn:
        # reseting driving clock
        Drive_Clock.pause()
        Drive_Clock.reset()

        # reseting variables
        ForcedTurn = False
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
        if CC.DrivingStage in CC.DoNotTurn:
            print("skipping turning")
            robot.straight(75)

        elif CC.DrivingStage in CC.ReverseTurns:
            ServoTurn(-2,3,60)
        else:
            ServoTurn(-2,3,-60)

        # specific driving stage things
        if CC.DrivingStage == 4 or CC.DrivingStage == 6:
            robot.reset()

        Dumping_Clock.pause()
        Dumping_Clock.reset()

    # driving stage logic
    if   CC.DrivingStage == 1: ## Sensor follow
        Follow_Ultra( CC.StageValues[CC.DrivingStage] )
    elif CC.DrivingStage == 2: ## Mechanical follow
        Follow_Mechanical()
    elif CC.DrivingStage == 3: ## Mechanical follow
        Follow_Mechanical()
    elif CC.DrivingStage == 4: ## Mechanical follow with distnace measurement
        driven = robot.distance()
        Follow_Mechanical()

        if driven >= CC.StageValues[4]:
            ForcedTurn = True
    elif CC.DrivingStage == 5: ## Sensor follow
        Follow_Ultra( CC.StageValues[CC.DrivingStage] )
    elif CC.DrivingStage == 6: ## Mechanical follow backwards & distance measurement
        Reverse_Follow_Mechanical()
    elif CC.DrivingStage == 7: ## Dumping balls
        SortingMotor.run_until_stalled(-1*CC.SortSpeed, Stop.COAST, 40)
        Dumping_Clock.resume()

        print('dumping')
        if Dumping_Clock.time() >= CC.DumpTime:
            ForcedTurn = True
    elif CC.DrivingStage == 8: ## Mechanical follow
        Follow_Mechanical()
    elif CC.DrivingStage == 9: ## Dumping balls
        SortingMotor.run_until_stalled(CC.SortSpeed, Stop.COAST, 40)
        Dumping_Clock.resume()

        print('dumping')
        if Dumping_Clock.time() >= CC.DumpTime:
            ForcedTurn = True

    else:
        break
    
    # constant time program cycle
    if Cycle_Clock.time() < CC.LoopTime: # spare time -> waits
        wait(CC.LoopTime - Cycle_Clock.time())
    else: # not enought time
        print('\033Err: cycle took to long!\033') # printing in red color
        print(Cycle_Clock.time())
    
    Cycle_Clock.reset()
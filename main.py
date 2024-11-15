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

    reverse_dist = 40 # in mm

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

def Follow_Ultra(Stage):
        # dist = InfraSensor.distance()
        dist = UlraSensor.distance()
        error = CC.StageValues[Stage] - dist/10 # dividing by 10 'cause ultrasonic sensor gives answer in mm -- delete the dividing when working with infraRed

        lenght = len(CC.DistanceAvrg)
        sum = 0

        if lenght == 0: # creates an average value of last 5
            CC.DistanceAvrg.append(error)
            num = error
        else:
            if lenght == CC.Values_in_Avrg:
                CC.DistanceAvrg.pop(0)
            CC.DistanceAvrg.append(error)

            for i in CC.DistanceAvrg:
                sum += i
            num = sum/(lenght + 1)
            
        correction_Angle =  -1 * (num**CC.expKoef) * CC.linKoef # INVERTED!!!

        correction_Angle = CC.MaxCorrection if correction_Angle > CC.MaxCorrection else correction_Angle

        if error < 0:
            print("target to right")
        else:
            print("target to left")
        print('err: ',round(error, 2),'avrg: ', round(num, 2),'result: ', round(correction_Angle, 3))
        return correction_Angle

def Follow_Mechanical():
    global Fixing
    if SideBtn.pressed(): # if True then we are directly next to wall
        robot.drive(True_Drive_Speed, CC.FollowAngle['ok'])
        Fixing = 0
    else: # if True then we are directly next to wall
        if not Fixing:
            Drive_Clock.reset()
            Drive_Clock.resume()
            Fixing = 1
            robot.drive(True_Drive_Speed, CC.FollowAngle['btn-off'])
        elif Drive_Clock.time() > 1000:
            robot.drive(True_Drive_Speed, 0)

##--##--##--## CHECKING THE COLORS ##--##--## 
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
            print("ERROR: unknown color: ", DetectedColor) # quite common - TODO: change sth to make it rarer
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

# driving
ForcedTurn = False
Drive_Clock = StopWatch()
Fixing = 0 # zero.. everything ok; 1 or -1 ... a problem - trying to drive back

Drive_Clock.pause()
Drive_Clock.reset()

# color sorting
Now_Sorting = False
Back_Direction = None

Sort_Clock = StopWatch()
Sort_Clock.pause()
Sort_Clock.reset()

Game_Clock = StopWatch()

CC.StageValues[1] = UlraSensor.distance()/10


while True: # change to True to run
    if Game_Clock.time() < 1000:
        True_Drive_Speed = Game_Clock.time()/1000 * CC.DriveSpeed

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
        Drive_Clock.pause()
        Drive_Clock.reset()
        Fixing = 0

        CC.DrivingStage += 1
        # forced stop
        if CC.DrivingStage == CC.StopAt:
            break

        robot.stop()
        Ev3.speaker.beep()
        ServoTurn(400,-90)

        if CC.DrivingStage == 4:
            robot.reset()
        elif CC.DrivingStage == 5:
            ForcedTurn = False


    if   CC.DrivingStage == 1: ## Sensor follow
        # Following wall with infrared sensor
        angle = Follow_Ultra( CC.DrivingStage )

        robot.drive(True_Drive_Speed, angle)
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
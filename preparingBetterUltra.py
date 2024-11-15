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
LeftMotor = Motor( RC.Motors['left'],positive_direction = Direction.COUNTERCLOCKWISE )
RightMotor = Motor( RC.Motors['right'],positive_direction = Direction.COUNTERCLOCKWISE )

robot = DriveBase( LeftMotor, RightMotor, RC.Wheel_Diameter, RC.Axle_Track )

# Sensors
FrontBtn = TouchSensor( RC.Buttons['front'] )
SideBtn = TouchSensor( RC.Buttons['side'] )

# Gyro = GyroSensor( RC.Gyro_port )
# InfraSensor = InfraredSensor( RC.InfraSensor_port )
UlraSensor = UltrasonicSensor( RC.UlraSensor_port )


##--##--##--## Funcions ##--##--##--##
def Turn(Angle): # NOT-USED
    robot.straight(-10)
    robot.stop()
    
    Angle -= CC.TurnErr*Angle
    
    direction = 1 if Angle > 0 else -1
    print('in func; gyro before: ',Gyro.angle(),'target angle: ', Angle)
    Gyro.reset_angle(0)
    
    curentAngle = Gyro.angle()
    print('current angle: ', curentAngle )
    LastAngle = curentAngle
    while abs(curentAngle) < abs(Angle):
        robot.drive(0, -45*direction)
        curentAngle = Gyro.angle()
        if curentAngle != LastAngle:
            print('current angle: ', curentAngle )
            LastAngle = curentAngle
    
    robot.stop()

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

        if lenght == 0: # there are no values in average
            CC.DistanceAvrg.append(error)
            correction_Angle = error
        else: # there is sth. in average
            if lenght == CC.Values_in_Avrg: # if the list is full enought we can DELETE OLD VALUES
                CC.DistanceAvrg.pop(0)
            CC.DistanceAvrg.append(error)

            for i in CC.DistanceAvrg: # sum of all values
                sum += i
            correction_Angle = sum/lenght
        
        # the turning angle
        num = -1 * (error**CC.expKoef) * CC.linKoef # INVERTED!!!

        # helping robot to get back to target distance if it is off by a lot
        if num >= CC.MaxCorrection or Fixing:
            
            if not Fixing: # the error was found right now
                Drive_Clock.reset()
                Drive_Clock.resume()

                Fixing = 1  # TODO: -1 or 1 based on if i am higher or lower then target
                
                num =  CC.FollowAngle['btn-off']
                CC.DistanceAvrg = []
                
            elif Drive_Clock.time() > 1000: # after some time the robot is at corect angle - now he will drive straight forward until he is at right distance from wall
                num = 0
            elif abs(error) <= CC.Toleration:
                num = CC.FollowAngle
                
                
        else:
            Fixing = 0
            Drive_Clock.pause()
            Drive_Clock.reset()


        
        print('err: ',error,'measured koef: ', num,'final koef: ', correction_Angle)
        return correction_Angle

def Follow_Mechanical():
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

##--##--##--## GAME LOOP ##--##--##--##
# Ev3.speaker.beep()
ForcedTurn = False
Drive_Clock = StopWatch()
Fixing = 0 # zero.. everything ok; 1 or -1 ... a problem - trying to drive back

Drive_Clock.pause()
Drive_Clock.reset()

while True: # change to True to run

    # stop the program detection
    if FrontBtn.pressed() or ForcedTurn:
        Drive_Clock.pause()
        Drive_Clock.reset()
        Fixing = 0

        robot.stop()
        Ev3.speaker.beep()
        ServoTurn(400,-90)

        CC.DrivingStage += 1
        if CC.DrivingStage == 4:
            robot.reset()
        elif CC.DrivingStage == 5:
            ForcedTurn = False

    if   CC.DrivingStage == 1: ## Sensor follow
        # Following wall with infrared sensor
        angle = Follow_Ultra( CC.DrivingStage )

        robot.drive(CC.DriveSpeed, angle)
    elif CC.DrivingStage == 2: ## Mechanical follow
        Follow_Mechanical()
    elif CC.DrivingStage == 3: ## Mechanical follow
        Follow_Mechanical()
    elif CC.DrivingStage == 4: ## Mechanical follow with distnace measurement
        ahead = robot.distance()
        print('ahead', ahead,'done?: ', ahead >= CC.StageValues[4])
        Follow_Mechanical()

        if ahead >= CC.StageValues[4]:
            ForcedTurn = True
    else:
        dist = UlraSensor.distance()
        print('wall distance after last turn: ', dist)
        break
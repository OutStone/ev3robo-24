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
FrontBtn =  TouchSensor( RC.Buttons['front'] )
Gyro = GyroSensor( RC.Gyro_port )
#InfraSensor = InfraredSensor( RC.InfraSensor_port )
UlraSensor = UltrasonicSensor( RC.UlraSensor_port )


##--##--##--## Funcions ##--##--##--##
def Turn(Angle):
    Angle -= CC.TurnErr*Angle
    
    direction = 1 if Angle > 0 else -1
    print('in func',Gyro.angle(), Angle)
    Gyro.reset_angle(0)
    
    curentAngle = Gyro.angle()
    print( curentAngle )
    LastAngle = curentAngle
    while abs(curentAngle) < abs(Angle):
        robot.drive(0, -45*direction)
        curentAngle = Gyro.angle()
        if curentAngle != LastAngle:
            print( curentAngle )
            LastAngle = curentAngle
    
    robot.stop()

def Turn_in_Motion( A, B, Speed, Angle ):
    Gyro.reset_angle(0)

    curentAngle = Gyro.angle()
    print( curentAngle )
    LastAngle = curentAngle

    while abs(curentAngle) < abs(Angle):
        LeftMotor.speed(A*Speed)
        RightMotor.speed(B*Speed)
        
        curentAngle = Gyro.angle()
        if curentAngle != LastAngle:
            print( curentAngle )
            LastAngle = curentAngle
    
    robot.stop()

def Follow(Stage):
       # dist = InfraSensor.distance()
        dist = UlraSensor.distance()
        error = CC.StageValues[Stage] - dist/10 # dividing by 10 'cause ultrasonic sensor gives answer in mm -- delete the dividing when working with infraRed

        num = -1 * (error**CC.expKoef) * CC.linKoef # INVERTED!!!

        num = CC.MaxCorrection if num > CC.MaxCorrection else num # checkk if works

        lenght = len(CC.DistanceAvrg)
        sum = 0

        if lenght == 0:
            CC.DistanceAvrg.append(num)
            correction_Angle = num
        else:
            if lenght == CC.Values_in_Avrg:
                CC.DistanceAvrg.pop(0)
            CC.DistanceAvrg.append(num)

            for i in CC.DistanceAvrg:
                sum += i
            correction_Angle = sum/lenght

        
        print(error, num, correction_Angle)
        return correction_Angle

##--##--##--## GAME LOOP ##--##--##--##
Ev3.speaker.beep()
ForcedTurn = False

while True:

    # stop the program detection
    if FrontBtn.pressed() or ForcedTurn:
        robot.stop()
        Ev3.speaker.beep()
        Turn(-90)
        CC.DrivingStage += 1
        if CC.DrivingStage == 4:
            robot.reset()
        elif CC.DrivingStage == 5:
            ForcedTurn = False

    if   CC.DrivingStage == 1: ## Sensor follow
        # Following wall with infrared sensor
        angle = Follow( CC.DrivingStage )

        robot.drive(CC.DriveSpeed, angle)
    elif CC.DrivingStage == 2: ## Mechanical follow
        robot.drive(CC.DriveSpeed, -10)
    elif CC.DrivingStage == 3: ## Mechanical follow
        robot.drive(CC.DriveSpeed, -10)
    elif CC.DrivingStage == 4: ## Mechanical follow with distnace measurement
        ahead = robot.distance()
        print(ahead, ahead >= CC.StageValues[4])
        robot.drive(CC.DriveSpeed, -10)

        if ahead >= StageValues[4]:
            ForcedTurn = True
    else:
        break
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

def ServoTurn( Speed, Angle ): # in mm & deg
    # equation for number of wheel turns ( x )
    # x = (Turning radius/wheel radius) * (turning angle/360 deg)

    reverse_dist = 15 # in mm

    robot.straight(-1*reverse_dist)
    robot.stop()

    if Angle > 0: # turning left - left wheel stands
        Can_Left = 0
        Can_Right = 1
    else: # turning right
        Can_Left = 1
        Can_Right = 0

    Radius_Ratio = RC.Axle_Track/(RC.Wheel_Diameter/2)
    print(Radius_Ratio)
    Angle_Fraction = Angle/360

    Left_Angle = Can_Left * (Angle_Fraction * Radius_Ratio) * 360
    Right_Angle = Can_Right * (Angle_Fraction * Radius_Ratio) * 360


    print("zacatek zataceni")
    LeftMotor.run_angle(  Left_Angle  )
    RightMotor.run_angle( Right_Angle )

    print("konec zataceni")
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

        
        print('err: ',error,'measured koef: ', num,'final koef: ', correction_Angle)
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
        #OneWheelTurn(300, -90)
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
        print('ahead', ahead,'done?: ', ahead >= CC.StageValues[4])
        robot.drive(CC.DriveSpeed, -10)

        if ahead >= CC.StageValues[4]:
            ForcedTurn = True
    else:
        break
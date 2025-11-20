#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Port

Motors = {
    'drive' : Port.A,
    'arm'   : Port.B,
    'third' : Port.C
}
Buttons = {
    '1'  : Port.S1,
    '2'  : Port.S2 
}

ColorSensor_port = Port.S3
Gyro_port = Port.S3 # Not on robot

InfraSensor_port = Port.S4 # Not on robot
UlraSensor_port = Port.S4

ArmWheelDiameter = 42 # in mm
Wheel_Diameter = 35 # in mm
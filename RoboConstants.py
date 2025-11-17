#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Port

Motors = {
    'drive' : Port.A,
    'arm'   : Port.D,
    'third' : Port.B
}
Buttons = {
    'front' : Port.S2,
    'side'  : Port.S2 
}

ColorSensor_port = Port.S3
Gyro_port = Port.S3 # Not on robot

InfraSensor_port = Port.S4 # Not on robot
UlraSensor_port = Port.S1

ArmWheelDiameter = 24 # in mm
Wheel_Diameter = 50 # in mm #TODO: check 
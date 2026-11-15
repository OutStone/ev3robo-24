#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Port

Motors = {
    'rotor'  : Port.B,
    '1'   : Port.A,
    '2'   : Port.D
}
Buttons = {
    '1'  : Port.S1
}

ColorSensor_port = Port.S3 # Not on robot 
Gyro_port        = Port.S3 # Not on robot

InfraSensor_port = Port.S4 # Not on robot
UlraSensor_port  = Port.S4 # Not on robot
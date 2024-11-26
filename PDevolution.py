import math
TARGET = 700 # in mm - every distance measurement is in MILIMETERS
DRIVESPEED = 400 # deg/s - anglar turning speed of the wheels
AXEL_TRACK = 100
WHEEL_RADIUS = 50
GAMECYCLE_TIME = 20/1000 # in seconds

def UltrasonicSensor(x,angle):
        distance = x/math.cos(angle)
        if distance > 2550:
            return 2550
        else:
            return distance

def UltrasonicPos(Pos,Off):
    deltaX = Off.x * math.cos(Pos.angle) + Off.y * math.sin(Pos.angle)
    deltaY = Off.x * math.sin(Pos.angle) + Off.y * math.cos(Pos.angle)

    B = {
        'x' : Pos.x + deltaX;
        'y' : Pos.y + deltaY
    }

    return B

def PD(previous_error,Pos, Koefs):
    global previous_error
    dist = UltrasonicSensor(Pos.x,Pos.angle)

    error = TARGET - dist

    derivative = error - previous_error

    correction = Koefs.p * error + Koefs.d * derivative
    previous_error = error

    speeds = {
        'left' : DRIVESPEED + correction,
        'right': DRIVESPEED - correction
    }
    return speeds

def Movement(speeds,Pos):
    
    # cinverting speeds from angluar speed of the wheel to velocities
    speeds.left = 2 * WHEEL_RADIUS * math.pi * (speeds.left/360)
    speeds.right = 2 * WHEEL_RADIUS * math.pi * (speeds.right/360)


    radius_left = (AXEL_TRACK * speeds.left) / speeds.right - speeds.left # negative value means it is in the direction to the other wheel
    radius_fromCentre = radius_left + (AXEL_TRACK/2)

    TurnPoint = {
        'x' : Pos.x + radius_fromCentre * math.sin(Pos.angle),
        'y' : Pos.y + radius_fromCentre * math.cos(Pos.angle)
    }

    drivenDistance = ((speeds.left + speeds.right)/2) * GAMECYCLE_TIME

    drivenAngle = (2 * radius_fromCentre * math.pi) / (drivenDistance) # in radeans TODO: convert it!
import math
TARGET = 700 # in mm - every distance measurement is in MILIMETERS
DRIVESPEED = 100#400 # deg/s - anglar turning speed of the wheels
AXEL_TRACK = 100
WHEEL_RADIUS = 50
GAMECYCLE_TIME = 20/1000 # in seconds
SENSOROFFSET = {
    'x' : -100,
    'y' : 100
}

def UltrasonicSensor(x,angle): #returns value from distance in the same format as real sensor would do it
        distance = x/math.cos(angle)
        if distance > 2550:
            return 2550
        else:
            return distance

def UltrasonicPos(Pos,Off): # returns position of ultrasonic sensor
    invert = 1

    if Pos['angle'] > 90:
        Pos['angle'] = 180 - Pos['angle']
        invert = -1
    elif Pos['angle'] < -90:
        Pos['angle'] = -180 - Pos['angle']

    deltaX = Off['x'] * math.cos(Pos['angle']) * invert + Off['y'] * math.sin(Pos['angle'])
    deltaY = Off['x'] * math.sin(Pos['angle']) + invert * Off['y'] * math.cos(Pos['angle'])

    B = {
        'x' : Pos['x'] + deltaX,
        'y' : Pos['y'] + deltaY
    }

    return B

def PD(previous_error,Pos,Ultra, Koefs): # returns speeds of wheels and error value 
    dist = UltrasonicSensor(Ultra['x'],Pos['angle'])

    print('dist: ',dist)
    error = TARGET - dist

    derivative = error - previous_error

    correction = Koefs['p'] * error + Koefs['d'] * derivative
    previous_error = error

    speeds = {
        'left' : DRIVESPEED + correction,
        'right': DRIVESPEED - correction
    }
    return [speeds,error]

def Movement(speeds,Pos): # return new position
    
    # converting speeds from angluar speed of the wheel to velocities
    speeds['left'] = 2 * WHEEL_RADIUS * math.pi * (speeds['left']/360)
    speeds['right'] = 2 * WHEEL_RADIUS * math.pi * (speeds['right']/360)

    print('real speeds:',speeds)

    radius_left = (AXEL_TRACK * speeds['left']) / speeds['right'] - speeds['left'] # negative value means it is in the direction to the other wheel     TODO:BROKEN!!
    radius_fromCentre = radius_left + (AXEL_TRACK/2)
    
    print('radius_lefts:',radius_left,'radius_fromCentre:',radius_fromCentre)

    
    # solwing a problem with angle not beeing in range of 90 to -90
    invert = 1
    workAngle = Pos['angle']

    if workAngle > 90:
        workAngle= 180 - workAngle
        invert = -1
    elif workAngle < -90:
        workAngle = -180 - workAngle

    TurnPoint = {
        'x' : Pos['x'] + radius_fromCentre * math.sin(workAngle) * invert,
        'y' : Pos['y'] + radius_fromCentre * math.cos(workAngle) * invert
    }

    # Driven angle
    drivenDistance = ((speeds['left'] + speeds['right'])/2) * GAMECYCLE_TIME
    drivenAngle = 360 * (drivenDistance) /(2 * radius_fromCentre * math.pi)

    if radius_left > 0:
        drivenAngle *= -1
    
    Pos['angle'] += drivenAngle

    # New position
    deltaX = radius_fromCentre * math.cos(workAngle + drivenAngle) * invert
    deltaY = radius_fromCentre * math.sin(workAngle + drivenAngle)

    return {
        'x' : Pos['x'] + deltaX,
        'y' : Pos['y'] + deltaY,
        'angle': Pos['angle']
    }

def Drive(Koefs, StartPos, numOfCycles):
    robot = StartPos
    averageErr = 0
    lastErr = 0

    for cycle in range(numOfCycles):
        Ultra = UltrasonicPos(robot,SENSOROFFSET)
        print('Ultra:',Ultra)
        Speeds,Err = PD(lastErr,robot,Ultra,Koefs)
        print('speeds:',Speeds,'err:',Err)
        robot = Movement(Speeds,robot)
        print('robot:',robot)
        lastErr = Err
        
        averageErr = (averageErr*cycle + Err)/(cycle+1)
        print('avrg: ', averageErr)

    return averageErr

print( Drive({
    'p' : 0.5, # koefs
    'd' : 4.5
}, {
    'x' : 600, # robo pos
    'y' : 0,
    'angle' : 0
}, 2)
)
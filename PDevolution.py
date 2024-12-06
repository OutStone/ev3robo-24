import math
import random

import os
os.remove("stats.txt") # ensures we have a clear text file
file = open("stats.txt", "a")

TARGET = 500 # in mm - every distance measurement is in MILIMETERS
DRIVESPEED = 400#400 # deg/s - anglar turning speed of the wheels
AXEL_TRACK = 100
WHEEL_RADIUS = 50
GAMECYCLE_TIME = 20/1000 # in seconds
SENSOROFFSET = {
    'x' : 0,
    'y' : 0
}

def sin(a):
    val = a * math.pi/180
    return math.sin(val)
def cos(a):
    val = a * math.pi/180
    return math.cos(val)

# the driving part
def UltrasonicSensor(x,angle): #returns value from distance in the same format as real sensor would do it
        distance = x/cos(angle)
        if distance > 2550 or distance < 0:
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

    deltaX = Off['x'] * cos(Pos['angle']) * invert + Off['y'] * sin(Pos['angle'])
    deltaY = Off['x'] * sin(Pos['angle']) + invert * Off['y'] * cos(Pos['angle'])

    B = {
        'x' : Pos['x'] + deltaX,
        'y' : Pos['y'] + deltaY
    }

    return B

def PD(previous_error,Pos,Ultra, Koefs): # returns speeds of wheels and error value 
    dist = UltrasonicSensor(Ultra['x'],Pos['angle'])

    error = TARGET - dist

    if previous_error == None:
        derivative = 0
    else:
        derivative = error - previous_error

    correction = Koefs['p'] * error + Koefs['d'] * derivative
    previous_error = error

    speeds = {
        'left' : DRIVESPEED - correction,
        'right': DRIVESPEED + correction
    }
    return [speeds,error]

def Movement(speeds,Pos): # return new position
    
    # converting speeds from angluar speed of the wheel to velocities
    speeds['left'] = 2 * WHEEL_RADIUS * math.pi * (speeds['left']/360)
    speeds['right'] = 2 * WHEEL_RADIUS * math.pi * (speeds['right']/360)
    if speeds['left'] - speeds['right'] == 0:
        distance = speeds['left'] * GAMECYCLE_TIME
        NewX = Pos['x'] + sin(Pos['angle']) * distance
        NewY = Pos['y'] + cos(Pos['angle']) * distance

        return {
            'x' : NewX,
            'y' : NewY,
            'angle': Pos['angle']
        }

    else:
        radius_right = -1 * (AXEL_TRACK * speeds['right']) / (speeds['left'] - speeds['right']) # negative value means it is in the direction from the other wheel
        radius_fromCentre = radius_right - (AXEL_TRACK/2)
        
        # solwing a problem with angle not beeing in range of 90 to -90
        beforeAngle = Pos['angle']

        # Driven angle
        drivenDistance = ((speeds['left'] + speeds['right'])/2) * GAMECYCLE_TIME
        if radius_fromCentre == 0:
            Pos['angle'] += 360 * (drivenDistance) / (2 * radius_right * math.pi)
            return Pos
        else:
            drivenAngle = 360 * (drivenDistance) / (2 * radius_fromCentre * math.pi)

            Pos['angle'] += drivenAngle

            # New position
            NewX = Pos['x'] + radius_fromCentre * cos(beforeAngle) - radius_fromCentre * cos(Pos['angle'])
            NewY = Pos['y'] - radius_fromCentre * sin(beforeAngle) + radius_fromCentre * sin(Pos['angle'])
            

            return {
                'x' : NewX,
                'y' : NewY,
                'angle': Pos['angle']
            }

def Drive(StartPos, Koefs, numOfCycles):
    trajectory = []
    robot = StartPos
    averageErr = 0
    lastErr = None
    ErrSum = 0
    trajectory.append(  [robot['x'],robot['y']] )

    for cycle in range(numOfCycles):
        Ultra = UltrasonicPos(robot,SENSOROFFSET)
        Speeds,Err = PD(lastErr,ErrSum,robot,Ultra,Koefs)
        robot = Movement(Speeds,robot)
        lastErr = Err
        ErrSum += Err
        averageErr += abs(Err) # used for rating

        trajectory.append(  [robot['x'],robot['y']] )

    return averageErr,trajectory

# drawing the trajectory
def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb 


from tkinter import *

win=Tk()
win.geometry("1500x1000")
canvas=Canvas(win, width=3000, height=1000)
canvas.pack()

StartColor = (0,100,0)
MaxRGB = 255

# target line
canvas.create_line(0, TARGET - SENSOROFFSET['x'],  3000, TARGET - SENSOROFFSET['x'],fill=_from_rgb((255,0,0)),width=1)

def graph(points,color):
    for i in range(len(points)-1):
        canvas.create_line(points[i][1]+100, points[i][0], points[i+1][1]+100, points[i+1][0],fill=_from_rgb(color),width=1)
        win.update()
        

# the evolution part
def evolution():
    InGen = 100
    genNum = 100
    GensToResetStart = 5
    DrawingFrequency = 1
    PrecisionFrequency = 100
    RangeP = 10
    RangeD = 20
    CyclesInRun = 200
    StartPos = {
        'x' : 400, # robo pos from wall
        'y' : 0,
        'angle' : 0
    }

    KoefList = [ { 'p': 1*random.uniform(0,100),'d': 1*random.uniform(0,100)} for i in range(InGen)]

    for gen in range(genNum):
        minErrOfGen = None

        for KoefSet in KoefList:
            err,trajectory = Drive(StartPos,KoefSet,CyclesInRun)
            if minErrOfGen == None or err < minErrOfGen:
                Best = {
                    'err' : err,
                    'koefs' : KoefSet,
                    'trajectory' : trajectory
                }
                minErrOfGen = err

        print('best of gen',gen,'is',Best['err'],'and its koefs are', Best['koefs'])
        file.write(str(Best) + '\n')

        
        Kp = Best['koefs']['p']
        Kd = Best['koefs']['d']
        Ki = Best['koefs']['i']
        KoefList = [ {'p': Kp*random.uniform(1-RangeP,1+RangeP),
                    'd': Kd*random.uniform(1-RangeD,1+RangeD)}
                    for i in range(InGen-1)
                    ]
        KoefList.append({
            'p' : Kp,
            'd' : Kd
        })

        if gen % DrawingFrequency == 0:
            ColorStep = round((255/(genNum/DrawingFrequency)) * gen/DrawingFrequency)
            drawColor = (0,100, ColorStep)
            graph(Best['trajectory'], drawColor)

        if gen % PrecisionFrequency == 0 and gen != 0:
            RangeP /= 2
            RangeD /= 2
        # if gen % GensToResetStart == 0 and gen != 0:
        #     minimum = 8#math.ceil(SENSOROFFSET['x']/100) + 1
        #     maximum = math.ceil(TARGET/100) + 5
        #     StartPos['x'] = 100 * random.randint(minimum,maximum)
        #     print('---start reset',StartPos['x']/100)

    file.close()
    print(Best)

evolution()
# err,trajectory = Drive({
#         'x' : 400, # robo pos from wall
#         'y' : 0,
#         'angle' : 0
#     },{'p':11.5, 'd': 12},
#           200)
# graph(trajectory,(0,0,255))
# err,trajectory = Drive({
#         'x' : 400, # robo pos from wall
#         'y' : 0,
#         'angle' : 0
#     },{'p': 11.55530954020414, 'd': 11.69120644342326},
#           200)
# graph(trajectory,(0,255,0))
win.mainloop()
import math
import random

import os
os.remove("stats.txt") # ensures we have a clear text file
file = open("stats.txt", "a")

# varibles for robot
TARGET = 700 # in mm - every distance measurement is in MILIMETERS
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

    B = {
        'x' : Pos['x'] - cos(Pos['angle']) * Off['x']  + sin(Pos['angle']) * Off['y'],
        'y' : Pos['y'] + sin(Pos['angle']) * Off['x'] +  cos(Pos['angle']) * Off['y']

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
    return speeds,error

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

def Scoring(Ultra,ScoreSum,cycle,Pos):
    return (ScoreSum*cycle + (abs(Ultra['x'] - TARGET)/10)**2)/(cycle + 1)


def Drive(StartPos, Koefs, numOfCycles): # manages the looping of functions for simulating a driving robot
    trajectory = []
    robot = StartPos
    lastErr = None
    Score = 0
    ErrList = []
    trajectory.append(  [robot['x'],robot['y']] )

    for cycle in range(numOfCycles):
        Ultra = UltrasonicPos(robot,SENSOROFFSET)
        Speeds,lastErr = PD(lastErr,robot,Ultra,Koefs)

        robot = Movement(Speeds,robot)
        Score = Scoring(Ultra,Score,cycle,robot)

        #ErrList.append([err + 400,robot['y']])
        trajectory.append(  [robot['x'],robot['y']] )

    return Score,trajectory#,ErrList

# drawing the trajectory
def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb 


from tkinter import *

DriveWin=Tk()
DriveWin.title('Trajectories')
DriveWin.geometry("1500x1000")
DriveCanvas=Canvas(DriveWin, width=4000, height=1000)
DriveCanvas.pack()

GenWin = Tk()
GenWin.title('err')
GenCanvas=Canvas(GenWin, width=4000, height=1000)
GenCanvas.pack()

StartColor = (0,100,0)
MaxRGB = 255

# target and visualization lines line
DriveCanvas.create_line(0, (TARGET - SENSOROFFSET['x'])/2,  3000, (TARGET - SENSOROFFSET['x'])/2,fill=_from_rgb((255,0,0)),width=1)
DriveCanvas.create_line(   0, 1000-250, 1000, 1000-250,fill=_from_rgb((0,0,0)),width=1)
DriveCanvas.create_line(1000, 1000-500, 1000, 1000-250,fill=_from_rgb((0,0,0)),width=1)

GenCanvas.create_line(  0, (TARGET - SENSOROFFSET['x'])/2,  3000, (TARGET - SENSOROFFSET['x'])/2,fill=_from_rgb((255,0,0)),width=1)
GenCanvas.create_line(  0, (TARGET - SENSOROFFSET['x'])/2,  3000, (TARGET - SENSOROFFSET['x'])/2,fill=_from_rgb((255,0,0)),width=1)

def graph(points,color,window,canvas):
    for i in range(len(points)-1):
        canvas.create_line(points[i][1]/2+100, points[i][0]/2, points[i+1][1]/2+100, points[i+1][0]/2,fill=_from_rgb(color),width=1)
    window.update()

def scoreGraph(val,gen,genNum,color,window,canvas):
    lenght = 1000/genNum
    canvas.create_line(lenght * gen,1000-(250 + val/2),lenght * (gen + 1),1000-(250 + val/2),fill=_from_rgb(color),width=1)
    window.update()

# the evolution part
def evolution():
    InGen = 100
    genNum = 100
    CyclesInRun = 500
    StartPos = {
        'x' : 400, # robo pos from wall
        'y' : 0,
        'angle' : 0
    }
    RangeP = 0.8
    RangeD = 0.8

    MainDrawingFrequency = 1
    GensToResetStart = None
    PrecisionFrequency = None
    DrawingEachTry = None
    DrawingEachColor = (0,255,0)

    KoefList = [ { 'p': 1*random.uniform(1-RangeP,1+RangeP),'d': 1*random.uniform(0,1)} for i in range(InGen)]

    for gen in range(genNum):
        minScoreOfGen = None

        i = 0
        for KoefSet in KoefList:
            score,trajectory = Drive(StartPos,KoefSet,CyclesInRun)
            if DrawingEachTry != None:
                graph(trajectory, DrawingEachColor,GenWin,GenCanvas)
                print(i)
                i += 1
            
            if minScoreOfGen == None or score < minScoreOfGen:
                Best = {
                    'score' : score,
                    'koefs' : KoefSet,
                    'trajectory' : trajectory
                }
                minScoreOfGen = score
                print('change in best')

        print('best of gen',gen,'is',Best['score'],'and its koefs are', Best['koefs'])
        file.write(str(Best) + '\n')

        scoreGraph(Best['score'],gen,genNum,(150,0,0),DriveWin,DriveCanvas) # score
        scoreGraph(Best['koefs']['p']*200,gen,genNum,(0,150,0),DriveWin,DriveCanvas) # p koef
        scoreGraph(Best['koefs']['d']*50,gen,genNum,(0,0,150),DriveWin,DriveCanvas) # d koef
        
        Kp = Best['koefs']['p']
        Kd = Best['koefs']['d']
        
        KoefList = [ {'p': Kp*random.uniform(1-RangeP,1+RangeP),
                    'd': Kd*random.uniform(1-RangeD,1+RangeD)}
                    for i in range(InGen)
                    ]

        if MainDrawingFrequency != None:
            if gen % MainDrawingFrequency == 0:
                ColorStep = round((255/(genNum/MainDrawingFrequency)) * gen/MainDrawingFrequency)
                drawColor = (0,100, ColorStep)
                graph(Best['trajectory'], drawColor,DriveWin,DriveCanvas)
        if DrawingEachTry != None:
            DrawingEachTry += 1
            if DrawingEachTry == 1:
                DrawingEachColor = (0,0,255)
            if DrawingEachTry == 2:
                sleep = input('go?:')
                DrawingEachColor = (0,255,0)
                GenCanvas.delete('all')
                DrawingEachTry = 0

        if PrecisionFrequency != None:
            if gen % PrecisionFrequency == 0 and gen != 0:
                RangeP /= 2
                RangeD /= 2
                print('---range reduced','p',RangeP,'d',RangeD)

        if GensToResetStart != None:
            if gen % GensToResetStart == 0 and gen != 0:
                minimum = 3
                maximum = 10
                StartPos['x'] = 100 * random.randint(minimum,maximum)
                print('---start reset',StartPos['x']/100)

    file.close()
    print(Best)

evolution()
# score,trajectory = Drive({
#         'x' : 400 + TARGET, # robo pos from wall
#         'y' : 0,
#         'angle' : 0
#     },{'p': 1.0789589068008072, 'd': 5.55470152884985},
#           300)
# print(trajectory)
# graph(trajectory,(0,0,255),DriveWin,DriveCanvas)
# score,trajectory = Drive({
#         'x' : 400, # robo pos from wall
#         'y' : 0,
#         'angle' : 0
#     },{'p': 0.44738445662399723, 'd': 5},
#           300)
# print(score)
# graph(trajectory,(0,255,0),DriveWin,DriveCanvas)
DriveWin.mainloop()
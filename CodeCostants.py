DriveSpeed = 300 # in mm/s
DrivingStage = 1 # changes with every turn
GamePart = 1
RunSecondPart = True

DistanceSensor_Offset = 10 # in cm from the ball eating part

StopAt = -1 # TESTING ONLY

Do_ColorSort = True 
StageValues = {
    1 : 70 - DistanceSensor_Offset, #- DistanceSensor_Offset, # Wall distance in cm 
    2 : None,
    3 : None,
    4 : 280 - 50, # Drive distance in mm
    5 : 42 - DistanceSensor_Offset, # Wall distance in cm # real value after last test 510mm
    6 : 5*1000, # time for backing
    7 : None, # dumping balls
    8 : None,
    9 : None, 
    10: 700, # Drive distance in mm
    11: 560,
    12:None
}
UltraFollowStages = [1,5]
ReverseTurns = [6,8]
DoNotTurn = [7,10,11]

##--##--## Constants for sorting 
SortSpeed = 1000 # in deg/s
SortAngle = {
    'red' : -950,
    'blue' : 500
}
SortToleration = 30 # in deg

DropPoints = {
    'red': -1200,
    'blue' : 1300
}
    ## sorting calibation
StartPos = -900
Force = 40

##--##--## Time Constants (in ms) ##--##--##
LoopTime = 20
DumpTime = 3 * 1000
GameLenght = 85 * 1000

##--##--## Constants for following wall with a sensor ##--##--##
proportial_gain = 5
integral_gain = 0 # useles for our needs
derivative_gain = 50

Kp2 = 6
Ki2 = 0 #-0.01
Kd2 = 70
##--##--## Constants for mechanical following ##--##--##
FollowAngle = {
    'ok' : 3,
    'btn-off' : -25
}
##--##--## Constants for turning function  ##--##--##
TurnErr = 10/9 #CHECK: check at the competition
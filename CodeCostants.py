DriveSpeed = 300 # in mm/s
DrivingStage = 1 # changes with every turn
GamePart = 1
RunSecondPart = True

DistanceSensor_Offset = 10 # in cm from the ball eating part

StopAt = -1 # TESTING ONLY

Do_ColorSort = True 
StageValues = {
    1 : None
}
UltraFollowStages = []
ReverseTurns = []
DoNotTurn = []

##--##--## Constants for gate operating 
GateSpeed = 500 # in deg/s
GateAngle = 360

##--##--## Time Constants (in ms) ##--##--##
LoopTime = 20
GameLenght = 90 * 1000

##--##--## Constants for following wall with a sensor ##--##--##
proportial_gain = 5
derivative_gain = 50

##--##--## Constants for mechanical following ##--##--##
FollowAngle = {
    'ok' : 3,
    'btn-off' : -25
}
##--##--## Constants for turning function  ##--##--##
TurnErr = 10/9 #CHECK: check at the competition
DriveSpeed = 800 # in mm/s
DrivingStage = 1 # changes with every turn

DistanceSensor_Offset = 10 # in cm from the ball eating part

Do_ColorSort = True 
StageValues = {
    1 : 70 - DistanceSensor_Offset, # Wall distance in cm 
    2 : None,
    3 : None,
    4 : 280, # Drive distance in mm
    5 : 42 - DistanceSensor_Offset, # Wall distance in cm # real value after last test 510mm
    6 : None,
    7 : None 
    # for eight I will need a drive distance again    
}

##--##--## Constants for sorting 
SortSpeed = 800 # in deg/s
SortTime = 450 # in miliseconds
SortAngle = {
    'red' : -230,
    'blue' : 70
}

##--##--## Constants for following wall with a sensor ##--##--##
WallDistance = 30 # in % from the sensors maximum
        # TODO: the distances will differ in value based on the drive line we are in
linKoef = 0.05
expKoef = 3

DistanceAvrg = []
Values_in_Avrg = 5 # 10 for infraRed
MaxCorrection = 70

##--##--## Constants for turning function  ##--##--##
TurnErr = 10/9 #TODO: check at the competition
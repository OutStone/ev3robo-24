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
SortSpeed = 1000 # in deg/s
SortTime = 370 # in miliseconds; 70 ms is a safety gap (sometimes the values are close to 340) 
SortAngle = {
    'red' : -70, ## -205 with reversed gear ratio (small to big)
    'blue' : 12 ## 40 with reversed gear ration (small to big)
}

##--##--## Constants for following wall with a sensor ##--##--##
linKoef = 0.05
expKoef = 3 

DistanceAvrg = []
Values_in_Avrg = 5 # 10 for infraRed
MaxCorrection = 70

##--##--## Constants for turning function  ##--##--##
TurnErr = 10/9 #CHECK: check at the competition
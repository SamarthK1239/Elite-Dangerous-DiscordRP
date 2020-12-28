import os
import glob

from pypresence import Presence
import time

list_of_files = glob.glob('C:/Users/samar/Saved Games/Frontier Developments/Elite Dangerous/*.log')

client_id = 793098629413208075
RPC = Presence(client_id)
RPC.connect()

def RichPresence(latest_file, CurrentState1):
    f = open(latest_file)
    with f as read_obj:
        for line in read_obj:
            if "StartJump" in line:
                Destination = line.split(",")
                x = len(Destination)
                if(x == 4):
                    StarSystem = Destination[3]
                    StarSystem = StarSystem[10: (len(StarSystem) - 1):]
                elif(x == 3):
                    StarSystem = Destination[2]
                    StarSystem = StarSystem[10: (len(StarSystem) - 1):]
                    #print("Jumping to " + StarSystem)
                CurrentState = "Jumping from " + StarSystem
                
                    
            elif "FSDJump" in line:
                Destination = line.split(",")
                StarSystem = Destination[2]
                StarSystem = StarSystem[15: (len(StarSystem) - 1):]
                #print("Jumped to " + StarSystem)
                if "Jumped" or "Supercruise" in CurrentState1:
                    CurrentState = "Supercruise in " + StarSystem
                else:
                    CurrentState = "Jumped to " + StarSystem
            elif "DockingGranted" in line:
                Details = line.split(",")
                StationName = Details[4]
                StationClass = Details[5]
                StationName = StationName[16: (len(StationName) - 1):]
                StationClass = StationClass[16: (len(StationClass) - 4)]
                #print("Docking at " +  StationName + " (" + StationClass + " Starport)")
                CurrentState = "Docking at " +  StationName + " (" + StationClass + " Starport)"
            elif "Docked" in line:
                Details = line.split(",")
                StationName = Details[2]
                StationClass = Details[3]
                System = Details[4]
                StationName = StationName[16: (len(StationName) - 1):]
                StationClass = StationClass[16: (len(StationClass) - 1)]
                System = System[15: (len(System) - 1):]
                #print("Docked at " +  StationName + " (" + StationClass + " Starport)" + "in " + System)
                CurrentState = "Docked at " +  StationName + " (" + StationClass + " Starport) " + "in " + System
            elif "SupercruiseEntry" in line:
                Details = line.split(",")
                System = Details[2]
                System = System[15: (len(System) - 1):]
                #print("Supercruise in " + System)
                CurrentState = "Supercruise in " + System
            elif "SupercruiseExit" in line:
                Details = line.split(",")
                System = Details[2]
                Body = Details[4]
                System = System[15: (len(System) - 1):]
                Body = Body[9: (len(Body) - 1)]
                BodyType = Details[6]
                BodyType = BodyType[13: (len(BodyType) - 4)]
                if(BodyType == "Station"):
                    BodyType = "Starport"
                if "supercruise" in CurrentState1:
                    CurrentState = "In Space near " + Body + " (" + BodyType + ")"
                else:
                    #print("Dropped supercruise at " + Body + "(" + BodyType + ")" + " in " + System)
                    CurrentState = "Dropped supercruise at " + Body + " (" + BodyType + ")" + " in " + System
    return CurrentState


latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

epoch = time.time()

f = open(latest_file)
with f as read_obj:
    for line in read_obj:
        if "GameMode" in line:
            Details = line.split(",")
            GameMode = Details[12]
            GameMode = "Playing " + GameMode[13: (len(GameMode) - 1):]
            print(GameMode)
CurrentState1 = ""            
f = open(latest_file)
num_lines = sum(1 for line in f)
while True:
    CurrentState = RichPresence(latest_file, CurrentState1)
    CurrentState1 = CurrentState
    print(CurrentState1)
    RPC.update(state=GameMode, details=CurrentState, large_image="logo", start=epoch)
    time.sleep(15)
    

            

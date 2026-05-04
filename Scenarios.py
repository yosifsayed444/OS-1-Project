from aglorithm.round_robin import process

def Scenario_A():
    return[
        process("P1",0,5) ,
        process("P2",1,3) ,
        process("P3",2,11)
    ]

def Scenario_B():
    return[
        process("P1",0,12) ,
        process("P2",0,4) ,
        process("P3",0,3)
    ]

def Scenario_C():
    return[
        process("P1",0,5) ,
        process("P2",1,3) ,
        process("P3",2,10) ,
        process("P4",3,2) ,
        process("P5",4,3)
    ]

def Scenario_D():
    return[
        process("P1",0,5) ,
        process("P2",1,3) ,
        process("P3",2,2) ,
        process("P4",3,4)
    ]

def Scenario_E():
    return[
        process("P1",-1,5) ,
        process("P2",2,-1) 
    ]

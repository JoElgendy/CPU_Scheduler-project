from Scheduler import Scheduler
from Process import Process

class Non_Pre_emptive_SJF (Scheduler): 
    def __init__(self): 
        Scheduler.__init__(self)
        self.time=0
        self.completed: list[Process] = []
        self.currentProcess= None 

    def allProcessesCompleted(self): 
        for process in self.processes:
            if not process.isCompleted():
                return False
        for process in self.arrived : 
            if process.remainingTime>0: 
                return False
        return True
    
    def update(self) : 
        for process in self.processes [:]: 
            # print(f"current pid is {process.pid}")
            if process.arrivalTime ==  self.time : 
                # print(f"current pid is {process.pid}")
                self.arrived.append(process)
                self.processes.remove(process)

        try : 
            if self.arrived[0].remainingTime == 0:  # el process ely kant shaghala da a5r time frame w mafrood a7awl 
                self.arrived[0].completionTime = self.time
                self.completed.append(self.arrived.pop(0))
                try : 
                    self.arrived.sort()
                    self.currentProcess = self.arrived[0].pid
                    self.arrived[0].remainingTime -= 1 
                except :
                    self.currentProcess = -1
            elif self.arrived[0].remainingTime > 0 : 
                print("ana hna ")
                self.arrived[0].remainingTime -= 1 
                self.currentProcess =  self.arrived[0].pid
        except : 
            self.currentProcess = -1
        print("5lsna unit time ")
        self.time+=1


    def scheduleStep(self):
        self.update()
        self.occupying.append(self.currentProcess)   

    def list_state (self): 
        print (f"current time is {self.time}")
        print ("processes in arrived:")
        for proc in self.arrived: 
            print(f"process : {proc.pid} and has remaining time : {proc.remainingTime}")
        print ("processes in waiting:")
        for proc in self.processes: 
            print(f"process : {proc.pid}")
        print ("processes in completed:")
        for proc in self.completed: 
            print(f"process : {proc.pid}")
        print("--------------------------------------")
        
"""
Use case to check the program 
"""
p1 = Process(1,0,2)
p2 = Process(2,0,5)
p3 = Process(3,3,2)

sched = Non_Pre_emptive_SJF()
sched.addProcess(p1)
sched.addProcess(p2)
sched.addProcess(p3)
# sched.addProcess(Process(4,0,1))

while not(sched.allProcessesCompleted()): 
    sched.list_state()
    sched.scheduleStep()
    if sched.time == 12 : 
        break

print(sched.occupying)

# for process in sched.arrived: 
#     print(f"process {process.pid} has remaining time = {process.remainingTime}")
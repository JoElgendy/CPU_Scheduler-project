from Scheduler import Scheduler
from Process import Process

class SJF_pre (Scheduler): 
    def __init__(self): 
        Scheduler.__init__(self)
        self.time=0
        self.completed: list[Process] = []
    def allProcessesCompleted(self): 
        for process in self.processes:
            if not process.isCompleted():
                return False
        for process in self.arrived : 
            if process.remainingTime>0: 
                return False
        return True
    def update(self) : 
        for proc in self.processes: 
            if proc.arrivalTime ==  self.time : 
                self.arrived.append(proc)
                self.processes.remove(proc)
            # else : 
                # proc.arrivalTime-=1
        self.arrived.sort() # will sort 
        try:
            self.currentProcess = self.arrived[0].pid
            
            self.arrived[0].remainingTime -= 1
            if(self.arrived[0].isCompleted()) :
                self.arrived[0].completionTime=self.time
                self.completed.append(self.arrived.pop(0))
            # pass
        except: 
            self.currentProcess = -1 
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
p2 = Process(2,1,4)
p3 = Process(3,4,1)

sched = SJF_pre()
sched.addProcess(p1)
sched.addProcess(p2)
sched.addProcess(p3)
# sched.addProcess(Process(4,0,1))

while not(sched.allProcessesCompleted()): 
    sched.scheduleStep()
    sched.list_state()
    if sched.time == 12 : 
        break

print(sched.occupying)

# for process in sched.arrived: 
#     print(f"process {process.pid} has remaining time = {process.remainingTime}")
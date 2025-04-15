from .Scheduler import Scheduler
from .Process import Process

class NonPreemptiveSJF(Scheduler): 
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
            if process.arrivalTime ==  self.time : 
                self.arrived.append(process)

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
                self.arrived[0].remainingTime -= 1 
                self.currentProcess =  self.arrived[0].pid
        except : 
            self.currentProcess = -1
        self.time+=1


    def scheduleStep(self):
        self.update()
        self.occupying.append(self.currentProcess)   

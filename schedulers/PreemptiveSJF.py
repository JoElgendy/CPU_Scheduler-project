from .Scheduler import Scheduler
from .Process import Process

class PreemptiveSJF(Scheduler): 
    def __init__(self): 
        Scheduler.__init__(self)
        self.time=0
        self.completed: list[Process] = []
    def allProcessesCompleted(self): 
        for process in self.processes:
            if not process.isCompleted():
                return False
        for process in self.arrived: 
            if process.remainingTime>0: 
                return False
        return True
    def update(self) : 
        for proc in self.processes:
            if proc.arrivalTime == self.time: 
                self.arrived.append(proc)
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

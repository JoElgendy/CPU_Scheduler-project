from Scheduler import Scheduler

class RoundRobin(Scheduler):
    def __init__(self, quantumTime):
        super().__init__()
        self.quantumTime = quantumTime
        self.remainQuantumTime = quantumTime
    
    def processToBeExecuted(self):
        raise("still to be implemented")            
           
    def scheduleStep(self): 
        while not super().allProcessesCompleted():
            super().arrivedHandler()
            self.processToBeExecuted()
            self.update()
        print("Scheduler is Done")

    def update(self):
        self.currentProcess.remaining_time -= 1
        self.remainQuantumTime -= 1
        self.currentTime += 1
        self.occupying.append(self.currentProcess.pid)
        if(self.currentProcess.isCompleted()):
            self.currentProcess.completionTime = self.currentTime      
        self.scheduleStep()










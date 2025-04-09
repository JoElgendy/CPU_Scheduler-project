from Scheduler import Scheduler

class RoundRobin(Scheduler):
    def __init__(self, quantumTime):
        super().__init__()
        self.quantumTime = quantumTime
        self.remainQuantumTime = quantumTime
        super().arrivedHandler()

        handler = {item: index for index, item in enumerate(self.arrived)}
        self.minPID = min(handler.keys())
        indexOfCurrentProcessID = handler[self.minPID]
        self.currentProcess = self.arrived[indexOfCurrentProcessID]
        self.nextPID = self.minPID + 1
    
    def processToBeExecuted(self):
        for process in self.arrived:
            if max(self.arrived, key=lambda p: p.pid).pid == self.currentProcess.pid:
                self.nextPID = min(self.arrived, key=lambda p: p.pid).pid

            matchingProcess = next((p for p in self.arrived if p.pid == self.nextPID), None)

            if(matchingProcess is not None):
                self.currentProcess = matchingProcess

            self.nextPID += 1
                
    
    def scheduleStep(self): 
            super().arrivedHandler()
            if self.currentProcess.isCompleted() or self.remainQuantumTime == 0:
                self.processToBeExecuted()
            else:
                pass
            self.update()
        print("Scheduler is Done")

    def update(self):
        self.currentProcess.remainingTime -= 1
        self.remainQuantumTime -= 1
        self.currentTime += 1
        self.occupying.append(self.currentProcess.pid)
        if(self.currentProcess.isCompleted()):
            self.currentProcess.completionTime = self.currentTime      
        self.scheduleStep()
from .Scheduler import Scheduler

class FCFS(Scheduler):
    nextPID = 0

    def __init__(self):
        super().__init__()
        self.idle = False

    def processToBeExecuted(self):
        while True:

            # Remove the completed process
            if(self.currentProcess.isCompleted()):
                try:
                    self.arrived.remove(self.currentProcess)
                except:
                    pass

            # Check if the next PID is in the arrived processes
            matchingProcess = next((p for p in self.arrived if p.pid == self.nextPID), None)

            # If a matching process is found, update the current process
            if matchingProcess is not None:
                self.currentProcess = matchingProcess
                self.nextPID += 1  
                break

            self.nextPID += 1      
    

    def scheduleStep(self):
        super().arrivedHandler()
        if(self.currentTime == 0) or self.idle == True:
            try:
                self.currentProcess = self.arrived[0]
                self.nextPID = self.currentProcess.pid + 1
                self.idle = False
            except:
                self.idle = True
                self.currentTime += 1
                return
            
        if self.currentProcess is not None and (self.currentProcess.isCompleted()):
            self.processToBeExecuted()

        if self.currentProcess is not None:
            self.update()

    def update(self):
        self.currentProcess.remainingTime -= 1
        self.currentTime += 1
        self.occupying.append(self.currentProcess.pid)
        if(self.currentProcess.isCompleted()):
            self.currentProcess.completionTime = self.currentTime      


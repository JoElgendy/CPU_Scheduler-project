from .Scheduler import Scheduler

class FCFS(Scheduler):

    def __init__(self):
        super().__init__()
        self.idle = False
        self.first = True

    def processToBeExecuted(self):
        while True:

            if not self.arrived:
                self.currentTime += 1
                self.occupying.append(-1)
                self.idle = True
                return
            else:
                self.idle = False
                # Remove the completed process
                if(self.currentProcess.isCompleted()) :
                    try:
                        self.arrived.remove(self.currentProcess)
                    except:
                        pass

                if len(self.arrived) != 0 :
                    matchingProcess = self.arrived[0]
                else :
                    matchingProcess = None


                # If a matching process is found, update the current process
                if matchingProcess is not None :
                    self.currentProcess = matchingProcess
                    break

    def scheduleStep(self):
        super().arrivedHandler()
        if ((self.currentTime == 0) or self.idle == True) and self.first :
            try:
                self.currentProcess = self.arrived[0]
                self.idle = False
                self.first = False
            except:
                self.currentTime += 1
                self.occupying.append(-1)
                self.idle = True
                self.first = True
                return

        if self.currentProcess is not None and (self.currentProcess.isCompleted()):
            self.processToBeExecuted()
            if self.idle:
                return

        if self.currentProcess is not None:
            self.update()

    def update(self):
        self.currentProcess.remainingTime -= 1
        self.currentTime += 1
        self.occupying.append(self.currentProcess.pid)
        if(self.currentProcess.isCompleted()):
            self.currentProcess.completionTime = self.currentTime      

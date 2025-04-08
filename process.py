class Process:
    def __init__(self, pid, arrivalTime, burstTime, priority=None):
        
        if burstTime <= 0:
            raise ValueError("Burst time must be positive")
        else:
            self.burstTime = burstTime

        if arrivalTime < 0:
            raise ValueError("Arrival time cannot be negative")
        else:
            self.arrivalTime = arrivalTime
        
        self.pid = pid
        self.remainingTime = burstTime
        self.priority = pid if priority is None else priority
        self.waitingTime = 0
        self.turnaroundTime = 0
        self.completionTime = 0
 
    def isCompleted(self) -> bool:
        # Check if the process has completed its execution
        return self.remainingTime == 0

    def decrementTime(self, time=1):
        """
        This is used to decrement time from the remaing time of the process
        to simulate running one timeunit on the processor 
        """
        if (self.remainingTime == 1): 
            self.remainingTime -= 1 
            self.completionTime = time + 1 
        else : 
            self.remainingTime -= 1

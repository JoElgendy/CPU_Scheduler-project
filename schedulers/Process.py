class Process:
    def __init__(self, pid, arrivalTime, burstTime=1, priority=None):
        
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
        """ 
        Check if the process has completed its execution  or not 
        """
        return self.remainingTime == 0
    
    def __gt__(self,other): 
        return (self.remainingTime > other.remainingTime)
    

    def __lt__(self, other ): 
        return (self.remainingTime < other.remainingTime )
    
    
    

        

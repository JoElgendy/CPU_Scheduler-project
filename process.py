class Process : 
    def __init__(self, pid, arrivalTime, burstTime, priority=None):
        self.pid = pid
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.remaining_time = burstTime
        self.priority = pid if priority is None else priority
        self.waitingTime = 0
        self.turnaroundTime = 0
        self.completionTime = 0
 
        

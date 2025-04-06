

class process : 
    def __init__(self, pid, arrival_time, burst_time, priority=None):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = pid if priority is None else priority
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0
 
        

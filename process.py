
class process : 
    pid = 0  
    incremental_pid =1  
    remaining_time = 0
    arrival_time = 0 
    completion_time  = 0
    burst_time = 0 
    priority = 1 

    def __init__(self , remaing_time , arrival_time) : 
        self.pid = self.incremental_pid 
        self.incremental_pid += 1 
        self.remaining_time =remaing_time 
        self.burst_time  = remaing_time 
        self.arrival_time = arrival_time

    
    def __init__(self , remaing_time , arrival_time, priority) : 
        self.pid = self.incremental_pid 
        self.incremental_pid += 1 
        self.remaining_time =remaing_time 
        self.burst_time  = remaing_time 
        self.arrival_time = arrival_time   
        self.priorty= priority  
        
    def decrement_time(self,current): 
        if ( self.remaining_time == 1 ) : 
            self.remaining_time -= 1 ; 
            self.completion_time = current + 1 
        else : 
            self.remaining_time -=1 


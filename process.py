class process :  
    """
    This is a class encapsulating all data and attributes of a process that, 
    we need in our CPU Process scheduler 

    We have made a class variable (incremental PID ) to auto distribute the pid on the created processes 
    """
    incremental_pid =1  

    def __init__(self , arrival, remaining =1 , priority =2 ) : 
        """
        This is the class constructor, in which we initialize all class attributes 
        """
        self.pid = self.incremental_pid 
        self.incremental_pid += 1 
        self.remaining_time =remaining
        self.burst_time  = remaining 
        self.arrival_time = arrival
        self.priortiy = priority

    def decrement_time(self,time=1): 
        """
        This is used to decrement time from the remaing time of the process
        to simulate running one timeunit on the processor 
        """
        if ( self.remaining_time == 1 ) : 
            self.remaining_time -= 1 ; 
            self.completion_time = time + 1 
        else : 
            self.remaining_time -=1 


p1 =process(1,0)
help(process)
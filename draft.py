class Scheduler:
    #occupying = [
    #  Each entry is a tuple of: (process_id, start_time, end_time)
    # ("P1", 0, 3),
    # ("P2", 3, 7),
    # ("P1", 7, 9),
#    p1>>>0 ,5                                 
#    p2>>>1 ,2
#    p3>>>1 ,2


    def __init__(self):
        self.occupying=[]
        self.processes = []
        self.cuurent_tmie=0  

    def add_process(self, process):
        self.processes.append(process)


    
    def calculate_metrics(self):
        total_waiting = 0
        total_turnaround = 0
        for process in self.processes:
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            total_waiting += process.waiting_time
            total_turnaround += process.turnaround_time
        
        avg_waiting = total_waiting / len(self.processes)
        avg_turnaround = total_turnaround / len(self.processes)
        return avg_waiting, avg_turnaround
    
    def schedule_step(self) #this should return the process object to be selected
        raise NotImplementedError("Must implement in subclass")
    
    def AllProcessesCompleted(self) -> bool:
            "it will be implemented here"
    def update(): #1)Advance the current_time 2) Update each process's state 3) Update the occupying list 4)Handle process additions
        raise NotImplementedError("Must implement in subclass")

    def run (self) : 
        # # Implement all steps 
        # # send for gui the occupying list 
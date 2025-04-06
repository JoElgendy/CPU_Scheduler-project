class Scheduler:
    #occupying = [
    #  Each entry is a tuple of: (process_id, start_time, end_time)
    # ("P1", 0, 3),
    # ("P2", 3, 7),
    # ("P1", 7, 9),
    # ............]
    #    p1>>>0 ,5                                 
    #    p2>>>1 ,2
    #    p3>>>1 ,2

    def __init__(self):
        self.occupying = []
        self.processes = []
        self.currentTime = 0    #Probably wont be needed in FCFS

    def addProcess(self, process):
        self.processes.append(process)


    
    def calculateMetrics(self):
        totalWaiting = 0
        totalTurnaround = 0
        for process in self.processes:
            process.turnaroundTime = process.completionTime - process.arrivalTime
            process.waitingTime = process.turnaroundTime - process.burstTime
            totalWaiting += process.waitingTime
            totalTurnaround += process.turnaroundTime
        
        avgWaiting = totalWaiting / len(self.processes)
        avgTurnaround = totalTurnaround / len(self.processes)
        return avgWaiting, avgTurnaround
    
    #This should return the process object to be selected to be given to the update
    def scheduleStep(self):  
        raise NotImplementedError("Must implement in subclass")
    

    def AllProcessesCompleted(self) -> bool:
        #it will be implemented here


    #1)Advance the current_time 2) Update each process's state 3) Update the occupying list 4)Handle process additions
    def update(self): 
        raise NotImplementedError("Must implement in subclass")
    

    def run (self) : 
        #Implement all steps 
        #send for gui the occupying list 


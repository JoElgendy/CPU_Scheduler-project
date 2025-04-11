from typing import final
from abc import ABC, abstractmethod

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

class Scheduler(ABC):
    #occupying 
    #  Each entry shows the process occupying the CPU at that time
    #  Suppose FCFS algorithm:
    #    p1>>>0 ,5                                 
    #    p2>>>1 ,2
    #    p3>>>1 ,2
    #    list should be as follows:
    #    occupying = [1,1,1,1,1,2,2,3,3]

    def __init__(self):
        self.occupying: list[int] = []      #Described above
        self.processes: list[Process] = []  #The initial processes given by the user
        self.arrived: list[Process] = []    #This que contains all arrived processes and process with remaining time to be executed    
        self.currentProcess: Process = None #Will contain the current process being executed
        self.currentTime: int = 0

    def allProcessesCompleted(self) -> bool:
    # Check if all processes have completed
        for process in self.processes:
            if not process.isCompleted():
                return False
        return True

    @final
    def addProcess(self, process: Process) -> None:
        # Add a new process to the scheduler
        if not isinstance(process, Process):
            raise TypeError("Expected a Process object")
        if process.isCompleted():
            raise ValueError("Process has already completed")
        self.processes.append(process)
    
    @final
    def calculateMetrics(self) -> tuple[float, float]:
        # Calculate average waiting time and turnaround time
        totalWaiting = 0.0
        totalTurnaround = 0.0
        for process in self.processes:
            process.turnaroundTime = process.completionTime - process.arrivalTime
            process.waitingTime = process.turnaroundTime - process.burstTime
            totalWaiting += process.waitingTime
            totalTurnaround += process.turnaroundTime
        
        avgWaiting = totalWaiting / len(self.processes)
        avgTurnaround = totalTurnaround / len(self.processes)
        return avgWaiting, avgTurnaround
    
    #This method pushes arrived processes into the arrived list and removes completed processes
    #This will method will ease the algo implementation
    @final
    def arrivedHandler(self) -> None:
        for process in self.processes:
            if(process.arrivalTime == self.currentTime):
                self.arrived.append(process)
    
    #This should save the process object in the variable current process to be selected to be given to the update
    @abstractmethod
    def scheduleStep(self) -> None:  
        raise NotImplementedError("Must implement in subclass")   

    # This method will be called in the main loop of the scheduler
    # It will call the scheduleStep method to get the next process to run
    # and then call the update method to update the state of the scheduler
    # and the processes
    #1)Advance the currentTime 2) Update each process's state 3) Update the occupying list 4)Handle process additions
    @abstractmethod
    def update(self) -> None: 
        raise NotImplementedError("Must implement in subclass")
    

    


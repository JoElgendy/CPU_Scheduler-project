from typing import final
from abc import ABC, abstractmethod
from Process import Process

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
        self.occupying: list[int] = []
        self.processes: list[Process] = []
        self.currentTime: int = 0

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
    
    #This should return the process object to be selected to be given to the update
    @abstractmethod
    def scheduleStep(self) -> Process:  
        raise NotImplementedError("Must implement in subclass")
    

    def allProcessesCompleted(self) -> bool:
        # Check if all processes have completed
        for process in self.processes:
            if not process.isCompleted():
                return False
        return True

    # This method will be called in the main loop of the scheduler
    # It will call the scheduleStep method to get the next process to run
    # and then call the update method to update the state of the scheduler
    # and the processes
    #1)Advance the currentTime 2) Update each process's state 3) Update the occupying list 4)Handle process additions
    @abstractmethod
    def update(self) -> None: 
        raise NotImplementedError("Must implement in subclass")
    


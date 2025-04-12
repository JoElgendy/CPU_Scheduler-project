from .Process import Process
from .Scheduler import Scheduler

class PriorityScheduler(Scheduler):
    def __init__(self, preemptive: bool=False):
        super().__init__()
        self.preemptive = preemptive

    def addProcess(self, process: Process) -> None:
        if process.burstTime == 0:
            print(f"Skipping Process {process.pid}: Burst time is zero.")
            return
        if process.isCompleted():
            raise ValueError("Process has already completed")
        self.processes.append(process)

    def update(self) -> None:
        # Remove completed processes
        self.arrived = [p for p in self.arrived if not p.isCompleted()]
        if not self.arrived:
            return

        self.arrived.sort(key=lambda p: p.priority)

        if self.preemptive:
            if self.currentProcess:
                if self.currentProcess.priority > self.arrived[0].priority:
                    self.arrived.append(self.currentProcess)
                    self.currentProcess = self.arrived.pop(0)
            else:
                self.currentProcess = self.arrived.pop(0)
        else:
            if not self.currentProcess:
                self.currentProcess = self.arrived.pop(0)

    def scheduleStep(self) -> None:
        self.arrivedHandler()
        self.update()

        if self.currentProcess:
            self.currentProcess.remainingTime -= 1
            self.occupying.append(self.currentProcess.pid)

            if self.currentProcess.isCompleted():
                self.currentProcess.completionTime = self.currentTime + 1
                self.currentProcess = None
        else:
            self.occupying.append(-1)

        self.currentTime += 1

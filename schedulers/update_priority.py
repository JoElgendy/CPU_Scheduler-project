import Processes.py
import Scheduler.py

class PriorityScheduler(Scheduler):
    def __init__(self, preemptive: bool):
        super().__init__()
        self.preemptive = preemptive
        
    def addProcess(self, process: Process) -> None:
        if process.burstTime == 0:
            print(f"Skipping Process {process.pid}: Burst time is zero.")
            return
        if process.isCompleted():
            raise ValueError("Process has already completed")
        self.processes.append(process)

    def scheduleStep(self) -> None:
        self.arrivedHandler()

        if self.arrived:
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

    def update(self) -> None:
        self.scheduleStep()

        if self.currentProcess:
            self.currentProcess.remainingTime -= 1
            self.occupying.append(self.currentProcess.pid)

            if self.currentProcess.isCompleted():
                self.currentProcess.completionTime = self.currentTime + 1
                self.currentProcess = None

        self.currentTime += 1

from typing import Optional, List
from abc import ABC, abstractmethod
import processes.py
import Scheduler.py

class PriorityScheduler(Scheduler):
    def __init__(self, preemptive: bool):
        super().__init__()
        self.preemptive = preemptive

    def update(self) -> None:
        self.arrivedHandler()

        if self.arrived:
            self.arrived.sort(key=lambda p: p.priority)

            if self.preemptive:
                if self.currentProcess and self.arrived and self.currentProcess.priority > self.arrived[0].priority:
                    self.arrived.append(self.currentProcess)
                    self.currentProcess = self.arrived.pop(0)
                elif not self.currentProcess:
                    self.currentProcess = self.arrived.pop(0)
            else:
                if not self.currentProcess:
                    self.currentProcess = self.arrived.pop(0)

        if self.currentProcess:
            self.currentProcess.remainingTime -= 1
            self.occupying.append(self.currentProcess.pid)  # Only log active process
            if self.currentProcess.isCompleted():
                self.currentProcess.completionTime = self.currentTime + 1
                self.currentProcess = None

        self.currentTime += 1


import heapq
import time
import threading
from Scheduler import Scheduler
from Process import Process
from typing import final


# Original PriorityScheduler Class (Inherits from Scheduler)
class PriorityScheduler(Scheduler):
    def __init__(self, preemptive=False, live=False, time_unit=1):
        super().__init__()
        self.ready_queue = []
        self.preemptive = preemptive
        self.live = live
        self.time_unit = time_unit
        self.running = False
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.currentProcess = None

    def scheduleStep(self) -> Process:
        if self.ready_queue:
            _, _, process = heapq.heappop(self.ready_queue)
            return process
        return None

    def update(self) -> None:
        with self.lock:
            for process in self.processes:
                if process.arrivalTime <= self.currentTime and not process.isCompleted() and \
                        all(p.pid != process.pid for _, _, p in self.ready_queue) and \
                        (self.currentProcess is None or self.currentProcess.pid != process.pid):
                    heapq.heappush(self.ready_queue, (process.priority, process.arrivalTime, process))

        if self.preemptive:
            # Preempt if higher priority is found
            if self.currentProcess:
                if self.ready_queue and self.ready_queue[0][0] < self.currentProcess.priority:
                    heapq.heappush(self.ready_queue, (self.currentProcess.priority, self.currentProcess.arrivalTime, self.currentProcess))
                    self.currentProcess = self.scheduleStep()
            else:
                self.currentProcess = self.scheduleStep()

        else:
            if self.currentProcess is None:
                self.currentProcess = self.scheduleStep()

        # Execute current process
        if self.currentProcess:
            self.occupying.append(self.currentProcess.pid)
            self.currentProcess.remainingTime -= 1
            if self.currentProcess.remainingTime == 0:
                self.currentProcess.completionTime = self.currentTime + 1
                self.currentProcess = None
        else:
            self.occupying.append(-1)  # idle

        self.currentTime += 1
        if self.live:
            time.sleep(self.time_unit)  # Sleep to simulate "live" behavior

    def run(self):
        self.running = True
        while self.running:
            if self.allProcessesCompleted():
                self.running = False
                break
            self.update()

    def addProcess(self, process: Process):
        with self.lock:
            super().addProcess(process)  # Call parent class's addProcess method
            print(f"Process {process.pid} added at time {self.currentTime}")
            self.event.set()


# Testing the inheritance and running the scheduler with dynamic additions
def test_dynamic_addition(preemptive=True, live=False):
    scheduler = PriorityScheduler(preemptive=preemptive, live=live, time_unit=1)

    scheduler.addProcess(Process(1, 3, 5, 0))
    scheduler.addProcess(Process(2, 0, 7, 1))

    scheduler_thread = threading.Thread(target=scheduler.run)
    scheduler_thread.start()

    time.sleep(2)
    if(scheduler.live==True):
        scheduler.addProcess(Process(3, scheduler.currentTime, 4, 0))
    
        time.sleep(2)
        scheduler.addProcess(Process(4, scheduler.currentTime, 3, 2))
    
        scheduler.addProcess(Process(5, scheduler.currentTime, 6, 1))

    scheduler_thread.join()

    print("\nGantt Chart:")
    for t, pid in enumerate(scheduler.occupying):
        if pid == -1:
            print(f"|{t}: Idle", end=" ")
        else:
            print(f"|{t}: P{pid}", end=" ")
    print(f"|{scheduler.currentTime}")

    avg_wt, avg_tat = scheduler.calculateMetrics()
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")
    
    all_done = all(p.isCompleted() for p in scheduler.processes)
    print(all_done)


if __name__ == "__main__":
    print("\n=== Running Preemptive Scheduling in Non-Live Mode ===")
    test_dynamic_addition(preemptive=True, live=False)

    print("\n=== Running Preemptive Scheduling in Live Mode ===")
    test_dynamic_addition(preemptive=True, live=True)

    print("\n=== Running Non-Preemptive Scheduling in Non-Live Mode ===")
    test_dynamic_addition(preemptive=False, live=False)

    print("\n=== Running Non-Preemptive Scheduling in Live Mode ===")
    test_dynamic_addition(preemptive=False, live=True)


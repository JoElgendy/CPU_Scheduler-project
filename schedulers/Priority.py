import heapq
import time

# Process Class
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.start_time = None
        self.completion_time = None

    def __lt__(self, other):
        # Processes with smaller priority number are given higher priority
        return (self.priority, self.arrival_time) < (other.priority, other.arrival_time)



class PriorityScheduler:
    def __init__(self, preemptive=False, live=False, time_unit=1):
        self.processes = []
        self.ready_queue = []
        self.current_time = 0
        self.preemptive = preemptive
        self.live = live
        self.time_unit = time_unit
        self.gantt_chart = []
        self.running = False

    def add_process(self, process):
        self.processes.append(process)

    def run(self):
        self.processes.sort(key=lambda p: p.arrival_time)  # Sort by arrival time
        arrived = []  # add to list when current time == arrived time 
        current_process = None
        self.running = True

        while True:
            # add arrived processes to ready queue
            for p in self.processes:
                if p.arrival_time == self.current_time and p not in arrived:
                    heapq.heappush(self.ready_queue, (p.priority, p.arrival_time, p))
                    arrived.append(p)

            # exit when all processes finish
            if not self.ready_queue and all(p.remaining_time == 0 for p in self.processes) and not current_process:
                self.running = False
                break

            if self.preemptive:
                #  preemptive
                if current_process:
                    if self.ready_queue and self.ready_queue[0][0] < current_process.priority:
                        # Preempt current process if new one has higher priority
                        heapq.heappush(self.ready_queue, (current_process.priority, current_process.arrival_time, current_process))
                        _, _, current_process = heapq.heappop(self.ready_queue)
                else:
                    if self.ready_queue:
                        _, _, current_process = heapq.heappop(self.ready_queue)
                        if current_process.start_time is None:
                            current_process.start_time = self.current_time

                # Execute the current process
                if current_process:
                    self.gantt_chart.append((self.current_time, current_process.pid))
                    current_process.remaining_time -= 1
                    if current_process.remaining_time == 0:
                        current_process.completion_time = self.current_time + 1
                        current_process = None

            else:
                # non-preemptive
                if current_process is None and self.ready_queue:
                    _, _, current_process = heapq.heappop(self.ready_queue)
                    if current_process.start_time is None:
                        current_process.start_time = self.current_time

                if current_process:
                    self.gantt_chart.append((self.current_time, current_process.pid))
                    current_process.remaining_time -= 1
                    if current_process.remaining_time == 0:
                        current_process.completion_time = self.current_time + 1
                        current_process = None

            # delay (live mode)
            if self.live:
                # Simulate the passage of time in live mode (allow for process addition)
                time.sleep(self.time_unit)

            # Increment the time for both modes
            self.current_time += 1
     




if __name__ == "__main__":

    scheduler = PriorityScheduler(preemptive=False, live=False)
    
    scheduler.add_process(Process(1, 0, 3, 2))  
    scheduler.add_process(Process(2, 1, 2, 1))  
    scheduler.add_process(Process(3, 2, 1, 3))  
    
    scheduler.run()
    
    scheduler.calculate_metrics()

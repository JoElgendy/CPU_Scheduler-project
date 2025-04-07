import heapq
import time
import threading


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
        # arranging processes inside heap --> least priority first 
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
        self.lock = threading.Lock()
        self.event = threading.Event()  # event to control thread pausing

    def add_new_process(self, process):
        # dynamic addition of processes
        with self.lock:
            self.processes.append(process)
            print(f"Process {process.pid} added at time {self.current_time}")
            self.event.set()  # Signal the run thread to resume

    def add_process(self, process):
        # for adding processes initially
        self.processes.append(process)

    def run(self):
        self.processes.sort(key=lambda p: p.arrival_time)  # sort by arrival time
        arrived = []  # track the arrived processes 
        current_process = None
        self.running = True

        while self.running:
            with self.lock:
                self.processes.sort(key=lambda p: p.arrival_time)

            for p in self.processes:
                if p.arrival_time <= self.current_time and p not in arrived: # less than in case that a process entered late 
                    heapq.heappush(self.ready_queue, (p.priority, p.arrival_time, p))
                    arrived.append(p)

            # in case no processes in queue && no current process running --> exit the loop 
            if not self.ready_queue and all(p.remaining_time == 0 for p in self.processes) and not current_process:
                self.running = False
                break

            if self.preemptive:
                #preemptive
                if current_process:
                    if self.ready_queue and self.ready_queue[0][0] < current_process.priority:
                        
                        heapq.heappush(self.ready_queue, (current_process.priority, current_process.arrival_time, current_process))
                        _, _, current_process = heapq.heappop(self.ready_queue)
                else:
                    if self.ready_queue:
                        _, _, current_process = heapq.heappop(self.ready_queue)
                        if current_process.start_time is None:
                            current_process.start_time = self.current_time

                # executing current process
                if current_process:
                    self.gantt_chart.append((self.current_time, current_process.pid))
                    current_process.remaining_time -= 1
                    if current_process.remaining_time == 0:
                        current_process.completion_time = self.current_time + 1
                        current_process = None

            else:
                #  non-preemptive 
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

            
            
            time.sleep(self.time_unit) # pausing the thread for new processes to be added ( for non-live & live mode ) 

            
            self.current_time += 1


    def calculate_metrics(self):
        total_wt = 0
        total_tat = 0
        for p in self.processes:
            if p.completion_time is None:
                continue  # Skip processes that have not completed
            tat = p.completion_time - p.arrival_time
            wt = tat - p.burst_time
            total_wt += wt
            total_tat += tat
        n = len(self.processes)
        return total_wt / n, total_tat / n

    def print_gantt_chart(self):
        print("Gantt Chart:")
        for t, pid in self.gantt_chart:
            print(f"|{t}: P{pid}", end=" ")
        print(f"|{self.current_time}")


# Testing Dynamic Addition

def test_dynamic_addition(preemptive=True, live=False):

    scheduler = PriorityScheduler(preemptive=preemptive, live=live, time_unit=1)

    # Initial processes
    scheduler.add_process(Process(1, 0, 5, 2))  # Process 1: Arrival at t=0, burst time=5, priority=2
    scheduler.add_process(Process(2, 0, 3, 1))  # Process 2: Arrival at t=0, burst time=3, priority=1

    # create and start a thread
    scheduler_thread = threading.Thread(target=scheduler.run)
    scheduler_thread.start()
    
    #adding new processes dynamically when the scheduler is running 
    
    time.sleep(2)  
    scheduler.add_new_process(Process(3, scheduler.current_time, 4, 0))  
    
    time.sleep(2) 
    scheduler.add_new_process(Process(4, scheduler.current_time, 3, 2))  

    
    scheduler.add_new_process(Process(5, scheduler.current_time, 6, 1))  
    
    # wait for thread to finish
    scheduler_thread.join()

    scheduler.print_gantt_chart()
    avg_wt, avg_tat = scheduler.calculate_metrics()
    print(f"Average Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")


if __name__ == "__main__":

    print("\n=== Running Preemptive Scheduling in Non-Live Mode ===")
    test_dynamic_addition(preemptive=True, live=False)  # preemptive & non-live

    print("\n=== Running Preemptive Scheduling in Live Mode ===")
    test_dynamic_addition(preemptive=True, live=True)  # preemptive & live

    print("\n=== Running Non-Preemptive Scheduling in Non-Live Mode ===")
    test_dynamic_addition(preemptive=False, live=False)  # non preemptive & non-live

    print("\n=== Running Non-Preemptive Scheduling in Live Mode ===")
    test_dynamic_addition(preemptive=False, live=True)  # non-preemptive & live

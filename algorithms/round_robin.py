class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0


def run_round_robin(processes, quantum):
    from collections import deque
    
    n = len(processes)
    time = 0
    completed = 0
    ready_queue = deque()
    gantt_chart = []
    
    processes.sort(key=lambda x: x.arrival_time)
    
    proc_idx = 0
    current_process = None
    
    while completed < n:
        while proc_idx < n and processes[proc_idx].arrival_time <= time:
            ready_queue.append(processes[proc_idx])
            proc_idx += 1
            
        if ready_queue:
            current_process = ready_queue.popleft()
            
            if not gantt_chart or gantt_chart[-1][1] != current_process.pid:
                gantt_chart.append((time, current_process.pid))
            
            execution_time = min(current_process.remaining_time, quantum)
            
            for _ in range(execution_time):
                time += 1
                while proc_idx < n and processes[proc_idx].arrival_time <= time:
                    ready_queue.append(processes[proc_idx])
                    proc_idx += 1
            
            current_process.remaining_time -= execution_time
            
            if current_process.remaining_time == 0:
                completed += 1
                current_process.completion_time = time
            else:
                ready_queue.append(current_process)
        else:
            if proc_idx < n:
                time = processes[proc_idx].arrival_time
            else:
                break
                
    for p in processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        
    return gantt_chart


def print_results(processes, gantt_chart):
    print("\nGantt Chart:")
    for t, pid in gantt_chart:
        print(f"| {pid} ", end="")
    print("|")

    print("\nProcess Details:")
    print("PID\tAT\tBT\tCT\tTAT\tWT")

    total_wt = 0
    total_tat = 0

    for p in processes:
        total_wt += p.waiting_time
        total_tat += p.turnaround_time
        print(f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t{p.completion_time}\t{p.turnaround_time}\t{p.waiting_time}")

    print(f"\nAverage Waiting Time = {total_wt / len(processes):.2f}")
    print(f"Average Turnaround Time = {total_tat / len(processes):.2f}")


if __name__ == "__main__":
    processes = [
        Process("P1", 0, 8),
        Process("P2", 1, 4),
        Process("P3", 2, 2),
        Process("P4", 3, 1)
    ]
    
    quantum = 2
    gantt = run_round_robin(processes, quantum)
    print_results(processes, gantt)
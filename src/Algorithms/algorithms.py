import collections
from src.model.process import Process

def simulate_rr(processes_input, quantum):
    processes = [Process(p.pid, p.arrival_time, p.burst_time) for p in processes_input]
    processes.sort(key=lambda x: x.arrival_time)
    time, ready_queue, gantt_chart, completed = 0, collections.deque(), [], 0
    n, idx = len(processes), 0
    ready_queue_history = []

    while completed < n:
        while idx < n and processes[idx].arrival_time <= time:
            ready_queue.append(processes[idx])
            idx += 1
        ready_queue_history.append((time, list(ready_queue)))
        if not ready_queue:
            if idx < n: 
                time = processes[idx].arrival_time
                continue
            else: 
                break
        curr = ready_queue.popleft()
        if curr.response_time == -1: 
            curr.response_time = time - curr.arrival_time
        exec_t = min(curr.remaining_time, quantum)
        gantt_chart.append((curr.pid, time, time + exec_t))
        for _ in range(exec_t):
            time += 1
            while idx < n and processes[idx].arrival_time <= time:
                ready_queue.append(processes[idx])
                idx += 1
        curr.remaining_time -= exec_t
        if curr.remaining_time == 0:
            curr.completion_time = time
            curr.turnaround_time = curr.completion_time - curr.arrival_time
            curr.waiting_time = curr.turnaround_time - curr.burst_time
            completed += 1
        else: 
            ready_queue.append(curr)
    return processes, gantt_chart, ready_queue_history

def simulate_srtf(processes_input):
    processes = [Process(p.pid, p.arrival_time, p.burst_time) for p in processes_input]
    n, time, completed, gantt_chart, last_pid, start_time = len(processes), 0, 0, [], -1, 0
    ready_queue_history = []
    
    while completed < n:
        avail = [p for p in processes if p.arrival_time <= time and p.remaining_time > 0]
        ready_queue_history.append((time, list(avail)))
        
        if not avail:
            next_a = min([p.arrival_time for p in processes if p.remaining_time > 0], default=None)
            if next_a is not None: 
                time = next_a
                continue
            else: 
                break
        curr = min(avail, key=lambda x: (x.remaining_time, x.arrival_time))
        if curr.response_time == -1: 
            curr.response_time = time - curr.arrival_time
        if curr.pid != last_pid:
            if last_pid != -1: 
                gantt_chart.append((last_pid, start_time, time))
            start_time, last_pid = time, curr.pid
        curr.remaining_time -= 1
        time += 1
        if curr.remaining_time == 0:
            curr.completion_time = time
            curr.turnaround_time = curr.completion_time - curr.arrival_time
            curr.waiting_time = curr.turnaround_time - curr.burst_time
            completed += 1
            gantt_chart.append((curr.pid, start_time, time))
            last_pid = -1
    return processes, gantt_chart, ready_queue_history

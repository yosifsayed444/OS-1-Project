def calculate_averages(processes):
    if not processes:
        return 0, 0, 0
    n = len(processes)
    avg_wt = sum(p.waiting_time for p in processes) / n
    avg_tat = sum(p.turnaround_time for p in processes) / n
    avg_rt = sum(p.response_time for p in processes) / n
    return avg_wt, avg_tat, avg_rt

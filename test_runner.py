from algorithms.round_robin import run_round_robin
from algorithms.srtf import run_srtf
from core.input_validation import validate_processes

def calculate_metrics(processes):
    total_wt = total_tat = total_rt = 0

    for p in processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

        total_wt += p.waiting_time
        total_tat += p.turnaround_time
        total_rt += p.response_time

    n = len(processes)
    return {
        "avg_wt": total_wt / n,
        "avg_tat": total_tat / n,
        "avg_rt": total_rt / n
    }

def run_test(name, processes, quantum):
    if not validate_processes(processes):
        print(f"{name}: Invalid Input ❌")
        return None

    import copy
    rr = copy.deepcopy(processes)
    srtf = copy.deepcopy(processes)

    rr_res = calculate_metrics(run_round_robin(rr, quantum))
    srtf_res = calculate_metrics(run_srtf(srtf))

    return rr_res, srtf_res
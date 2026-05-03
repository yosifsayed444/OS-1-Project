def calculate_metrics(processes, gantt):
    if not processes or not gantt:
        return {"processes": [], "avg_wt": 0, "avg_tat": 0, "avg_rt": 0}

    
    proc_info = _normalise_processes(processes)

 
    blocks = _normalise_gantt(gantt)


    _compute_per_process_metrics(proc_info, blocks)

    n = len(proc_info)
    avg_wt = sum(p["wt"] for p in proc_info) / n
    avg_tat = sum(p["tat"] for p in proc_info) / n
    avg_rt = sum(p["rt"] for p in proc_info) / n

    return {
        "processes": proc_info,
        "avg_wt": round(avg_wt, 2),
        "avg_tat": round(avg_tat, 2),
        "avg_rt": round(avg_rt, 2),
    }


def _normalise_processes(processes):
    result = []
    for p in processes:
        if isinstance(p, dict):
            result.append({
                "pid":     p.get("pid"),
                "arrival": p.get("arrival", p.get("arrival_time", 0)),
                "burst":   p.get("burst", p.get("burst_time", 0)),
            })
        else:
        
            result.append({
                "pid":     getattr(p, "pid", None),
                "arrival": getattr(p, "arrival_time", getattr(p, "arrival", 0)),
                "burst":   getattr(p, "burst_time", getattr(p, "burst", 0)),
            })
    return result
    
def _normalise_gantt(gantt):
    if not gantt:
        return []

    sample = gantt[0]

    # RR format
    if len(sample) == 3:
        return [(str(pid), int(start), int(end)) for pid, start, end in gantt]

    # SRTF format
    if len(sample) == 2:
        blocks = []

        for time, pid in gantt:
            if blocks and blocks[-1][0] == str(pid):
                continue
            blocks.append([str(pid), int(time)])

        for i in range(len(blocks) - 1):
            blocks[i].append(blocks[i + 1][1])

        if blocks:
            blocks[-1].append(blocks[-1][1] + 1)

        return [(b[0], b[1], b[2]) for b in blocks]

    return []


def _compute_per_process_metrics(proc_info, blocks):

    first_start = {} 
    last_end = {}    

    for pid, start, end in blocks:
        pid_str = str(pid)
        if pid_str not in first_start or start < first_start[pid_str]:
            first_start[pid_str] = start
        if pid_str not in last_end or end > last_end[pid_str]:
            last_end[pid_str] = end

    for p in proc_info:
        pid_str = str(p["pid"])

        # Completion Time
        ct = last_end.get(pid_str, 0)
        p["ct"] = ct

        # Turnaround Time = CT - Arrival Time
        tat = ct - p["arrival"]
        p["tat"] = tat

        # Waiting Time = TAT - Burst Time
        wt = tat - p["burst"]
        p["wt"] = wt

        # Response Time = First CPU start - Arrival Time
        rt = first_start.get(pid_str, 0) - p["arrival"]
        p["rt"] = rt
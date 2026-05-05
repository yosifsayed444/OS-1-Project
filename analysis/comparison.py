def best_waiting_time(rr_results, srtf_results):
    """
    Compare average waiting time between RR and SRTF.
    Returns a descriptive string with the winner and values.
    """
    rr_wt = rr_results.get("avg_wt", 0)
    srtf_wt = srtf_results.get("avg_wt", 0)

    if srtf_wt < rr_wt:
        return (
            f"Waiting Time: SRTF is better "
            f"(SRTF avg WT = {srtf_wt:.2f} vs RR avg WT = {rr_wt:.2f})"
        )
    elif rr_wt < srtf_wt:
        return (
            f"Waiting Time: Round Robin is better "
            f"(RR avg WT = {rr_wt:.2f} vs SRTF avg WT = {srtf_wt:.2f})"
        )
    else:
        return f"Waiting Time: Both algorithms are equal (avg WT = {rr_wt:.2f})"


def best_response_time(rr_results, srtf_results):
    """
    Compare average response time between RR and SRTF.
    Returns a descriptive string with the winner and values.
    """
    rr_rt = rr_results.get("avg_rt", 0)
    srtf_rt = srtf_results.get("avg_rt", 0)

    if rr_rt < srtf_rt:
        return (
            f"Response Time: Round Robin is better "
            f"(RR avg RT = {rr_rt:.2f} vs SRTF avg RT = {srtf_rt:.2f})"
        )
    elif srtf_rt < rr_rt:
        return (
            f"Response Time: SRTF is better "
            f"(SRTF avg RT = {srtf_rt:.2f} vs RR avg RT = {rr_rt:.2f})"
        )
    else:
        return f"Response Time: Both algorithms are equal (avg RT = {rr_rt:.2f})"


def check_fairness(rr_results):
    """
    Assess fairness of Round Robin by checking the spread (max - min)
    of waiting times across all processes.
    A smaller spread means more fairness.
    """
    processes = rr_results.get("processes", [])
    if not processes:
        return "Fairness: No process data available."

    wt_values = [p.get("wt", 0) for p in processes]
    wt_spread = max(wt_values) - min(wt_values)

    if wt_spread <= 2:
        verdict = "Round Robin appears FAIR — waiting times are close across all processes."
    elif wt_spread <= 6:
        verdict = "Round Robin appears MODERATELY FAIR — some variation in waiting times."
    else:
        verdict = "Round Robin appears LESS FAIR — noticeable variation in waiting times."

    return f"Fairness (RR WT spread = {wt_spread}): {verdict}"


def short_job_analysis(rr_results, srtf_results):
    """
    Compare TAT for short jobs (burst time <= 3) between RR and SRTF.
    Short jobs benefit more from SRTF due to preemption.
    """
    rr_processes = rr_results.get("processes", [])
    srtf_processes = srtf_results.get("processes", [])

    srtf_tat_by_pid = {
        str(p.get("pid")): p.get("tat", 0)
        for p in srtf_processes
    }

    short_jobs = [p for p in rr_processes if p.get("burst", 0) <= 3]

    if not short_jobs:
        return "Short Job Performance: No short jobs (burst <= 3) found in this workload."

    rr_short_avg_tat = sum(p.get("tat", 0) for p in short_jobs) / len(short_jobs)

    srtf_short_tats = [
        srtf_tat_by_pid[str(p.get("pid"))]
        for p in short_jobs
        if str(p.get("pid")) in srtf_tat_by_pid
    ]

    if not srtf_short_tats:
        return "Short Job Performance: Could not match short jobs between RR and SRTF."

    srtf_short_avg_tat = sum(srtf_short_tats) / len(srtf_short_tats)

    if srtf_short_avg_tat < rr_short_avg_tat:
        return (
            f"Short Job Performance: SRTF completes short jobs faster "
            f"(SRTF avg TAT = {srtf_short_avg_tat:.2f} vs RR avg TAT = {rr_short_avg_tat:.2f})"
        )
    else:
        return (
            f"Short Job Performance: RR is comparable for short jobs "
            f"(RR avg TAT = {rr_short_avg_tat:.2f} vs SRTF avg TAT = {srtf_short_avg_tat:.2f})"
        )


def quantum_effect_analysis(quantum, rr_results):
    """
    Analyze how the selected quantum affects Round Robin behavior.
    Smaller quantum = more context switches but better fairness.
    Larger quantum = fewer switches but RR behaves more like FCFS.
    """
    processes = rr_results.get("processes", [])
    if not processes:
        return f"Quantum Effect: Quantum = {quantum}, no process data to analyze."

    avg_burst = sum(p.get("burst", 0) for p in processes) / len(processes)

    if quantum <= avg_burst * 0.5:
        behavior = (
            f"Quantum ({quantum}) is small relative to avg burst ({avg_burst:.1f}). "
            "This causes frequent context switches, improving fairness but increasing overhead."
        )
    elif quantum >= avg_burst:
        behavior = (
            f"Quantum ({quantum}) is large relative to avg burst ({avg_burst:.1f}). "
            "Round Robin behaves similarly to FCFS with fewer preemptions."
        )
    else:
        behavior = (
            f"Quantum ({quantum}) is moderate relative to avg burst ({avg_burst:.1f}). "
            "Round Robin provides balanced fairness and efficiency."
        )

    return f"Quantum Effect: {behavior}"

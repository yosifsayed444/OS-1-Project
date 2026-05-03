import tkinter as tk

from gui.main_window import MainWindow
from algorithms.round_robin import run_round_robin
from algorithms.srtf import srtf_scheduling, Process
from core.metrics import calculate_metrics
from analysis.comparison import (
    best_waiting_time,
    best_response_time,
    check_fairness,
    short_job_analysis,
    quantum_effect_analysis
)
from analysis.conclusion import generate_conclusion


def run_simulation(processes, quantum, gui):

    if quantum <= 0:
        gui.show_error("Quantum must be greater than 0")
        return

    rr_procs = [Process(p['pid'], p['arrival'], p['burst']) for p in processes]
    rr_gantt = run_round_robin(rr_procs, quantum)

    srtf_procs = [Process(p['pid'], p['arrival'], p['burst']) for p in processes]
    srtf_gantt = srtf_scheduling(srtf_procs)

    rr_results = calculate_metrics(processes, rr_gantt)

    srtf_results = calculate_metrics(processes, srtf_gantt)

    gui.draw_rr_gantt(rr_gantt)

    gui.draw_srtf_gantt(srtf_gantt)

    gui.display_rr_results(rr_results)

    gui.display_srtf_results(srtf_results)


    rr_avg_wt = rr_results["avg_wt"]
    rr_avg_rt = rr_results["avg_rt"]

    srtf_avg_wt = srtf_results["avg_wt"]
    srtf_avg_rt = srtf_results["avg_rt"]


    waiting_result = best_waiting_time(
        rr_avg_wt,
        srtf_avg_wt
    )

    response_result = best_response_time(
        rr_avg_rt,
        srtf_avg_rt
    )

    fairness_result = check_fairness(
        rr_results["processes"]
    )

    short_job_result = short_job_analysis(
        srtf_results["processes"]
    )

    quantum_result = quantum_effect_analysis(
        quantum
    )

    conclusion_text = generate_conclusion(
        waiting_result,
        response_result,
        fairness_result,
        short_job_result,
        quantum_result
    )

    gui.display_comparison(
        waiting_result,
        response_result,
        fairness_result,
        short_job_result,
        quantum_result
    )

    gui.display_conclusion(
        conclusion_text
    )


def main():

    root = tk.Tk()

    gui = MainWindow(root)

    root.mainloop()


if __name__ == "__main__":
    main()
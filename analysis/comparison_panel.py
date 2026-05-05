import tkinter as tk
from analysis.comparison import (
    best_waiting_time,
    best_response_time,
    check_fairness,
    short_job_analysis,
    quantum_effect_analysis,
)
from analysis.conclusion import generate_conclusion


class ComparisonPanel:

    def __init__(self, root):
      
        tk.Label(
            root,
            text="Comparison Summary",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill="x", padx=10, pady=(10, 2))

        self.text = tk.Text(
            root,
            height=8,
            width=80,
            state="disabled",
            bg="#f5f5f5",
            relief="sunken",
            font=("Consolas", 10),
        )
        self.text.pack(padx=10, pady=(0, 8))

       
        tk.Label(
            root,
            text="Final Conclusion",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill="x", padx=10, pady=(0, 2))

        self.conclusion = tk.Text(
            root,
            height=6,
            width=80,
            state="disabled",
            bg="#f5f5f5",
            relief="sunken",
            font=("Consolas", 10),
        )
        self.conclusion.pack(padx=10, pady=(0, 10))


    def update(self, rr_results, srtf_results, quantum):
        """
        Called after a simulation run with the metrics dicts from
        core.metrics.calculate_metrics() for both algorithms.

        rr_results   – dict: {processes, avg_wt, avg_tat, avg_rt}
        srtf_results – dict: {processes, avg_wt, avg_tat, avg_rt}
        quantum      – int: the time quantum used for Round Robin
        """
        wt_line       = best_waiting_time(rr_results, srtf_results)
        rt_line       = best_response_time(rr_results, srtf_results)
        fairness_line = check_fairness(rr_results)
        short_line    = short_job_analysis(rr_results, srtf_results)
        quantum_line  = quantum_effect_analysis(quantum, rr_results)

        summary = "\n".join([wt_line, rt_line, fairness_line, short_line, quantum_line])
        conclusion_text = generate_conclusion(
            wt_line, rt_line, fairness_line, short_line, quantum_line
        )

        self._set_text(self.text, summary)
        self._set_text(self.conclusion, conclusion_text)

  
    def clear(self):
        """Reset both text boxes."""
        self._set_text(self.text, "")
        self._set_text(self.conclusion, "")

    @staticmethod
    def _set_text(widget, content):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, content)
        widget.config(state="disabled")

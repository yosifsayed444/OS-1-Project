import tkinter as tk
from tkinter import messagebox

from gui.gantt_chart import GanttChart, convert_srtf
from algorithms.round_robin import run_round_robin
from algorithms.srtf import srtf_scheduling, Process


class MainWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("RR vs SRTF Scheduler")

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Quantum:").grid(row=0, column=0)

        self.quantum_entry = tk.Entry(frame)
        self.quantum_entry.grid(row=0, column=1)

        run_btn = tk.Button(
            frame,
            text="Run Simulation",
            command=self.run_clicked
        )
        run_btn.grid(row=1, column=0, columnspan=2, pady=10)

    def run_clicked(self):

        try:
            quantum = int(self.quantum_entry.get())

            processes = [
                {"pid": "P1", "arrival": 0, "burst": 5},
                {"pid": "P2", "arrival": 1, "burst": 3}
            ]

            rr_processes = [
                Process(p["pid"], p["arrival"], p["burst"])
                for p in processes
            ]
            rr_raw = run_round_robin(rr_processes, quantum)
            rr_blocks = convert_srtf(rr_raw)

            srtf_processes = [
                Process(p["pid"], p["arrival"], p["burst"])
                for p in processes
            ]

            srtf_raw = srtf_scheduling(srtf_processes)
            srtf_blocks = convert_srtf(srtf_raw)

            rr_chart = GanttChart(self.root)
            rr_chart.draw(rr_blocks)

            srtf_chart = GanttChart(self.root)
            srtf_chart.draw(srtf_blocks)

        except:
            messagebox.showerror("Error", "Invalid Quantum")
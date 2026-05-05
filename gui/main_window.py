import tkinter as tk
from tkinter import messagebox, ttk

from gui.gantt_chart import GanttChart, convert_srtf
from gui.comparison_panel import ComparisonPanel
from gui.results_table import ResultsTable
from algorithms.round_robin import run_round_robin
from algorithms.srtf import srtf_scheduling, Process
from core.metrics import calculate_metrics


class AddProcessDialog(tk.Toplevel):
    """Small popup that asks for Arrival and Burst before adding a process."""

    def __init__(self, parent, pid):
        super().__init__(parent)
        self.title(f"Add Process {pid}")
        self.resizable(False, False)
        self.grab_set()          # modal
        self.result = None

        tk.Label(self, text=f"Process: {pid}", font=("Arial", 10, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(10, 6), padx=20
        )

        tk.Label(self, text="Arrival Time:").grid(row=1, column=0, sticky="e", padx=10, pady=4)
        self._arrival = tk.Entry(self, width=8)
        self._arrival.insert(0, "0")
        self._arrival.grid(row=1, column=1, padx=10, pady=4)

        tk.Label(self, text="Burst Time:").grid(row=2, column=0, sticky="e", padx=10, pady=4)
        self._burst = tk.Entry(self, width=8)
        self._burst.insert(0, "1")
        self._burst.grid(row=2, column=1, padx=10, pady=4)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Add", width=8, command=self._confirm,
                  bg="#4CAF50", fg="white").pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cancel", width=8, command=self.destroy).pack(side="left", padx=6)

        self._arrival.focus_set()
        self.bind("<Return>", lambda e: self._confirm())
        self.bind("<Escape>", lambda e: self.destroy())

        # center over parent
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width() // 2 - self.winfo_width() // 2
        py = parent.winfo_rooty() + parent.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{px}+{py}")

        self.wait_window(self)

    def _confirm(self):
        try:
            arrival = int(self._arrival.get())
            burst   = int(self._burst.get())
            if burst <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Arrival and Burst must be whole numbers, and Burst must be > 0.",
                                 parent=self)
            return
        self.result = (arrival, burst)
        self.destroy()


class MainWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("RR vs SRTF Scheduler")

        # ── Input area ──────────────────────────────────────────────────
        input_frame = tk.LabelFrame(root, text="Processes", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        self.tree = ttk.Treeview(
            input_frame,
            columns=("PID", "Arrival", "Burst"),
            show="headings",
            height=5,
        )
        for col, w in [("PID", 80), ("Arrival", 100), ("Burst", 100)]:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=w, anchor="center")
        self.tree.pack(fill="x")

        btn_frame = tk.Frame(input_frame)
        btn_frame.pack(pady=(5, 0))

        tk.Button(btn_frame, text="Add Process",
                  command=self._add_process).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Remove Selected",
                  command=self._remove_process).pack(side="left", padx=4)

        q_frame = tk.Frame(root)
        q_frame.pack(pady=5)
        tk.Label(q_frame, text="Quantum:").pack(side="left")
        self.quantum_entry = tk.Entry(q_frame, width=6)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.pack(side="left", padx=4)

        tk.Button(root, text="▶  Run Simulation",
                  command=self.run_clicked,
                  font=("Arial", 10, "bold"),
                  bg="#4CAF50", fg="white",
                  padx=10).pack(pady=6)

        self._pid_counter = 1

        # ── Gantt charts ────────────────────────────────────────────────
        tk.Label(root, text="Round Robin — Gantt Chart",
                 font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        self._rr_gantt = GanttChart(root)

        tk.Label(root, text="SRTF — Gantt Chart",
                 font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        self._srtf_gantt = GanttChart(root)

        # ── Results tables ──────────────────────────────────────────────
        self._rr_table   = ResultsTable(root, title="Round Robin — Results")
        self._srtf_table = ResultsTable(root, title="SRTF — Results")

        # ── Comparison panel ────────────────────────────────────────────
        self._comparison_panel = ComparisonPanel(root)

    # ───────────────────────────────────────────────────────────────────

    def _add_process(self):
        pid = f"P{self._pid_counter}"
        dlg = AddProcessDialog(self.root, pid)
        if dlg.result is None:
            return                          # user cancelled
        arrival, burst = dlg.result
        self.tree.insert("", "end", values=(pid, arrival, burst))
        self._pid_counter += 1

    def _remove_process(self):
        for item in self.tree.selection():
            self.tree.delete(item)

    def _get_processes(self):
        processes = []
        for item in self.tree.get_children():
            pid, arrival, burst = self.tree.item(item)["values"]
            processes.append({
                "pid":     str(pid),
                "arrival": int(arrival),
                "burst":   int(burst),
            })
        return processes

    def draw_rr_gantt(self, gantt):
        blocks = convert_srtf(gantt) if gantt and len(gantt[0]) == 2 else gantt
        if blocks:
            self._rr_gantt.draw(blocks)

    def draw_srtf_gantt(self, gantt):
        blocks = convert_srtf(gantt) if gantt and len(gantt[0]) == 2 else gantt
        if blocks:
            self._srtf_gantt.draw(blocks)

    def display_rr_results(self, results):
        self._rr_table.display(results)

    def display_srtf_results(self, results):
        self._srtf_table.display(results)

    def display_comparison(self, waiting, response, fairness, short_job, quantum_line):
        self._comparison_panel._set_text(
            self._comparison_panel.text,
            "\n".join([waiting, response, fairness, short_job, quantum_line])
        )

    def display_conclusion(self, conclusion_text):
        self._comparison_panel._set_text(
            self._comparison_panel.conclusion,
            conclusion_text
        )

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def run_clicked(self):
        try:
            quantum = int(self.quantum_entry.get())
        except ValueError:
            self.show_error("Quantum must be a whole number.")
            return

        processes = self._get_processes()
        if not processes:
            self.show_error("Please add at least one process.")
            return

        from main import run_simulation
        run_simulation(processes, quantum, self)

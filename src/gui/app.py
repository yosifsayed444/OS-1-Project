import tkinter as tk
from tkinter import ttk, messagebox
from src.model.process import Process
from src.Algorithms.algorithms import simulate_rr, simulate_srtf
from src.metrics.stats import calculate_averages
from src.tests.scenarios import SCENARIOS

class AlgorithmsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Round Robin vs SRTF")
        self.root.geometry("1200x900")
        self.processes_data = []
        self.setup_ui()

    def setup_ui(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=5)

        input_p = ttk.LabelFrame(top_frame, text="Input Panel")
        input_p.pack(fill="x", pady=5)
        
        row1 = ttk.Frame(input_p)
        row1.pack(fill="x", padx=5, pady=2)
        ttk.Label(row1, text="PID:").pack(side="left")
        self.pid_entry = ttk.Entry(row1, width=5)
        self.pid_entry.insert(0, "1")
        self.pid_entry.pack(side="left", padx=5)
        ttk.Label(row1, text="Arrival Time:").pack(side="left")
        self.arrival_entry = ttk.Entry(row1, width=8)
        self.arrival_entry.pack(side="left", padx=5)
        ttk.Label(row1, text="Burst Time:").pack(side="left")
        self.burst_entry = ttk.Entry(row1, width=8)
        self.burst_entry.pack(side="left", padx=5)
        ttk.Button(row1, text="Add Process", command=self.add_process).pack(side="left", padx=5)
        ttk.Button(row1, text="Reset", command=self.reset_inputs).pack(side="left", padx=5)
        
        ttk.Label(row1, text="Time Quantum:").pack(side="left", padx=(20, 0))
        self.quantum_entry = ttk.Entry(row1, width=8)
        self.quantum_entry.insert(0, "4")
        self.quantum_entry.pack(side="left", padx=5)
        ttk.Button(row1, text="Simulate", command=self.run_simulation).pack(side="left", padx=20)
        ttk.Button(row1, text="Clear All", command=self.clear_all).pack(side="left", padx=5)

        scenario_p = ttk.Frame(top_frame)
        scenario_p.pack(fill="x", pady=2)
        ttk.Label(scenario_p, text="Test Scenarios:").pack(side="left", padx=5)
        for s in ['A: Basic', 'B: Quantum Sens.', 'C: Short Job Heavy', 'D: Interactive Fairness', 'E: Validation']:
            ttk.Button(scenario_p, text=s, command=lambda x=s[0]: self.load_scenario(x)).pack(side="left", padx=2)

        self.process_table = ttk.Treeview(top_frame, columns=("PID", "Arrival", "Burst"), show="headings", height=4)
        for c in ["PID", "Arrival", "Burst"]: 
            self.process_table.heading(c, text=c)
            self.process_table.column(c, width=100)
        self.process_table.pack(fill="x", pady=5)

        results_container = ttk.Frame(self.root)
        results_container.pack(fill="both", expand=True, padx=10)
        
        rr_f = ttk.LabelFrame(results_container, text="Round Robin Results")
        rr_f.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ttk.Label(rr_f, text="Ready Queue Evolution (Snapshots):").pack(anchor="w", padx=5)
        self.rr_ready_view = tk.Text(rr_f, height=2, state="disabled", bg="#f8f8f8", font=("Consolas", 9))
        self.rr_ready_view.pack(fill="x", padx=5, pady=2)
        self.rr_gantt = tk.Canvas(rr_f, height=80, bg="white", borderwidth=1, relief="sunken")
        self.rr_gantt.pack(fill="x", padx=5, pady=5)
        self.rr_metrics_l = ttk.Label(rr_f, text="Avg WT: - | Avg TAT: - | Avg RT: -", font=("Arial", 10, "bold"))
        self.rr_metrics_l.pack(pady=2)
        self.rr_table = ttk.Treeview(rr_f, columns=("PID", "WT", "TAT", "RT"), show="headings", height=8)
        for c in self.rr_table["columns"]: 
            self.rr_table.heading(c, text=c)
            self.rr_table.column(c, width=60)
        self.rr_table.pack(fill="both", expand=True, padx=5, pady=5)

        srtf_f = ttk.LabelFrame(results_container, text="SRTF Results")
        srtf_f.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
        ttk.Label(srtf_f, text="Ready Queue Evolution (Snapshots):").pack(anchor="w", padx=5)
        self.srtf_ready_view = tk.Text(srtf_f, height=2, state="disabled", bg="#f8f8f8", font=("Consolas", 9))
        self.srtf_ready_view.pack(fill="x", padx=5, pady=2)
        self.srtf_gantt = tk.Canvas(srtf_f, height=80, bg="white", borderwidth=1, relief="sunken")
        self.srtf_gantt.pack(fill="x", padx=5, pady=5)
        self.srtf_metrics_l = ttk.Label(srtf_f, text="Avg WT: - | Avg TAT: - | Avg RT: -", font=("Arial", 10, "bold"))
        self.srtf_metrics_l.pack(pady=2)
        self.srtf_table = ttk.Treeview(srtf_f, columns=("PID", "WT", "TAT", "RT"), show="headings", height=8)
        for c in self.srtf_table["columns"]: 
            self.srtf_table.heading(c, text=c)
            self.srtf_table.column(c, width=60)
        self.srtf_table.pack(fill="both", expand=True, padx=5, pady=5)

        bottom_f = ttk.LabelFrame(self.root, text="Comparison Summary & Final Conclusion Area")
        bottom_f.pack(fill="x", padx=10, pady=10)
        self.conclusion_text = tk.Text(bottom_f, height=10, wrap="word", font=("Segoe UI", 10))
        self.conclusion_text.pack(fill="x", padx=5, pady=5)

    def add_process(self):
        try:
            pid_val = self.pid_entry.get().strip()
            arr_val = self.arrival_entry.get().strip()
            burst_val = self.burst_entry.get().strip()
            q_val = self.quantum_entry.get().strip()

            if not pid_val or not arr_val or not burst_val or not q_val:
                raise ValueError("All input fields (PID, Arrival, Burst, Quantum) are required.")

            pid = int(pid_val)
            a = int(arr_val)
            b = int(burst_val)

            if pid <= 0:
                raise ValueError("PID must be a positive integer.")
            if a < 0:
                raise ValueError("Arrival Time cannot be negative.")
            if b <= 0:
                raise ValueError("Burst Time must be a positive integer.")

            if any(p.pid == pid for p in self.processes_data):
                raise ValueError(f"Process ID {pid} already exists. Please use a unique ID.")

            self.processes_data.append(Process(pid, a, b))
            self.process_table.insert("", "end", values=(pid, a, b))
            
            self.pid_entry.delete(0, tk.END)
            self.pid_entry.insert(0, str(max([p.pid for p in self.processes_data] + [0]) + 1))
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    def reset_inputs(self):
        self.pid_entry.delete(0, tk.END)
        self.pid_entry.insert(0, str(max([p.pid for p in self.processes_data] + [0]) + 1))
        self.arrival_entry.delete(0, tk.END)
        self.burst_entry.delete(0, tk.END)

    def clear_all(self):
        self.processes_data = []
        for t in [self.process_table, self.rr_table, self.srtf_table]:
            for i in t.get_children(): t.delete(i)
        self.rr_gantt.delete("all")
        self.srtf_gantt.delete("all")
        for v in [self.rr_ready_view, self.srtf_ready_view]:
            v.config(state="normal")
            v.delete("1.0", tk.END)
            v.config(state="disabled")
        self.conclusion_text.delete("1.0", tk.END)
        
        
        self.rr_metrics_l.config(text="Avg WT: - | Avg TAT: - | Avg RT: -")
        self.srtf_metrics_l.config(text="Avg WT: - | Avg TAT: - | Avg RT: -")
       
       
        for entry in [self.pid_entry, self.arrival_entry, self.burst_entry, self.quantum_entry]:
            entry.delete(0, tk.END)
        
        self.pid_entry.insert(0, "1")

    def load_scenario(self, t):
        self.clear_all()
        if t == 'E': 
            for pid, arr, burst, q, desc in SCENARIOS['E']:
                messagebox.showinfo("Validation Test", f"Testing: {desc}")
                self.reset_inputs()
                self.pid_entry.delete(0, tk.END)
                self.pid_entry.insert(0, pid)
                self.arrival_entry.delete(0, tk.END)
                self.arrival_entry.insert(0, arr)
                self.burst_entry.delete(0, tk.END)
                self.burst_entry.insert(0, burst)
                self.quantum_entry.delete(0, tk.END)
                self.quantum_entry.insert(0, q)
                
                if desc == 'Invalid Quantum Value':
                    self.run_simulation()
                else:
                    self.add_process()
            return
        
        for a, b in SCENARIOS[t]:
            pid = len(self.processes_data) + 1
            self.processes_data.append(Process(pid, a, b))
            self.process_table.insert("", "end", values=(pid, a, b))
            
        if t == 'B': 
            self.quantum_entry.delete(0, tk.END)
            self.quantum_entry.insert(0, "2")
        messagebox.showinfo("Scenario Loaded", f"Scenario {t} Loaded.")

    def run_simulation(self):
        if not self.processes_data: 
            messagebox.showwarning("Empty", "Add processes first.")
            return
        try:
            q_val = self.quantum_entry.get().strip()
            if not q_val:
                raise ValueError("Time Quantum is required.")
            q = int(q_val)
            if q <= 0:
                raise ValueError("Time Quantum must be a positive integer.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
            
        rr_p, rr_g, rr_h = simulate_rr(self.processes_data, q)
        sr_p, sr_g, sr_h = simulate_srtf(self.processes_data)
        self.display(rr_p, rr_g, rr_h, sr_p, sr_g, sr_h)

    def display(self, rr_p, rr_g, rr_h, sr_p, sr_g, sr_h):
        for t in [self.rr_table, self.srtf_table]:
            for i in t.get_children(): t.delete(i)
            
        rw, rt, rr_avg = calculate_averages(rr_p)
        for p in rr_p:
            self.rr_table.insert("", "end", values=(p.pid, p.waiting_time, p.turnaround_time, p.response_time))
        self.rr_metrics_l.config(text=f"Avg WT: {rw:.2f} | Avg TAT: {rt:.2f} | Avg RT: {rr_avg:.2f}")
        self.draw_gantt(self.rr_gantt, rr_g)
        self.rr_ready_view.config(state="normal")
        self.rr_ready_view.delete("1.0", tk.END)
        hist = " -> ".join([f"T{t}:[{','.join([str(p.pid) for p in q])}]" for t, q in rr_h[:6]]) + " ..."
        self.rr_ready_view.insert("1.0", hist)
        self.rr_ready_view.config(state="disabled")

        sw, st, sr_avg = calculate_averages(sr_p)
        for p in sr_p:
            self.srtf_table.insert("", "end", values=(p.pid, p.waiting_time, p.turnaround_time, p.response_time))
        self.srtf_metrics_l.config(text=f"Avg WT: {sw:.2f} | Avg TAT: {st:.2f} | Avg RT: {sr_avg:.2f}")
        self.draw_gantt(self.srtf_gantt, sr_g)
        self.srtf_ready_view.config(state="normal")
        self.srtf_ready_view.delete("1.0", tk.END)
        s_hist = " -> ".join([f"T{t}:[{','.join([str(p.pid) for p in q])}]" for t, q in sr_h[:6]]) + " ..."
        self.srtf_ready_view.insert("1.0", s_hist)
        self.srtf_ready_view.config(state="disabled")
        
        self.summarize(rw, rt, rr_avg, sw, st, sr_avg)

    def draw_gantt(self, can, sch):
        can.delete("all")
        if not sch: return
        w = can.winfo_width() if can.winfo_width() > 100 else 550
        tot = sch[-1][2]
        if tot == 0: return
        sc = (w - 40) / tot
        cols = ["#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#9BF6FF", "#A0C4FF", "#BDB2FF", "#FFC6FF"]
        for pid, s, e in sch:
            x1, x2 = 20 + s * sc, 20 + e * sc
            can.create_rectangle(x1, 10, x2, 50, fill=cols[pid % len(cols)], outline="#333")
            can.create_text((x1+x2)/2, 30, text=f"P{pid}", font=("Arial", 9, "bold"))
            can.create_text(x1, 65, text=f"{s}", font=("Arial", 7))
        can.create_text(20 + tot * sc, 65, text=f"{tot}", font=("Arial", 7))

    def summarize(self, rw, rt, rr, sw, st, sr):
        q = self.quantum_entry.get()
        txt = f"REQUIRED ANALYSIS QUESTIONS & CONCLUSIONS\n" + "="*50 + "\n"
        txt += f"1. Better Avg Waiting Time? {'SRTF' if sw < rw else 'Round Robin'} ({min(sw,rw):.2f} vs {max(sw,rw):.2f})\n"
        txt += f"2. Better Response Time? {'Round Robin' if rr < sr else 'SRTF'} ({min(rr,sr):.2f} vs {max(rr,sr):.2f})\n"
        txt += f"3. Fairness: Round Robin is fairer as it distributes time slices ({q} units) to all jobs.\n"
        txt += f"4. SRTF efficiency: SRTF completes short jobs faster by prioritizing tasks.\n"
        txt += f"5. Quantum Effect: A quantum of {q} balance fairness vs overhead.\n"
        txt += f"6. Recommendation: Use SRTF for batch; use Round Robin for responsive systems.\n\n"
        txt += f"FINAL CONCLUSION:\n"
        txt += f"- SRTF was more efficient (Avg TAT: {st:.2f} vs {rt:.2f}).\n"
        txt += f"- Round Robin appeared fairer and better for first response time.\n"
        txt += f"- Observations: Preemption in SRTF prevents 'convoy effect' for short jobs."
        self.conclusion_text.delete("1.0", tk.END)
        self.conclusion_text.insert("1.0", txt)

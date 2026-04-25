import tkinter as tk
from tkinter import ttk

class InputPanel:

    def __init__(self, root):

        frame = tk.Frame(root)
        frame.pack(pady=10)

        
        self.tree = ttk.Treeview(
            frame,
            columns=("PID","Arrival","Burst"),
            show="headings"
        )

        self.tree.heading("PID", text="PID")
        self.tree.heading("Arrival", text="Arrival")
        self.tree.heading("Burst", text="Burst")

        self.tree.pack()

        
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        self.add_btn = tk.Button(
            btn_frame,
            text="Add Process",
            command=self.add_process
        )

        self.add_btn.pack(side="left")

        
        q_frame = tk.Frame(root)
        q_frame.pack()

        tk.Label(q_frame,
                 text="Quantum:").pack(side="left")

        self.quantum_entry = tk.Entry(q_frame)

        self.quantum_entry.pack(side="left")

        
        self.run_btn = tk.Button(
            root,
            text="Run Simulation"
        )

        self.run_btn.pack(pady=5)

        self.pid = 1

    def add_process(self):

        self.tree.insert(
            "",
            "end",
            values=(self.pid,0,0)
        )

        self.pid += 1
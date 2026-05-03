import tkinter as tk
from tkinter import ttk


class ResultsTable:

    def __init__(self, root, title="Results"):

        self.frame = tk.LabelFrame(root, text=title, padx=10, pady=10)
        self.frame.pack(fill="x", padx=10, pady=5)

        columns = ("PID", "Arrival", "Burst", "CT", "TAT", "WT", "RT")

        self.tree = ttk.Treeview(
            self.frame,
            columns=columns,
            show="headings",
            height=8,
        )

        col_widths = {
            "PID": 60,
            "Arrival": 70,
            "Burst": 70,
            "CT": 70,
            "TAT": 70,
            "WT": 70,
            "RT": 70,
        }

        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(
                col,
                width=col_widths.get(col, 80),
                anchor="center",
                minwidth=50,
            )

        self.tree.pack(fill="x")

        self.avg_label = tk.Label(
            self.frame,
            text="",
            anchor="w",
            justify="left",
            font=("Consolas", 10),
        )
        self.avg_label.pack(fill="x", pady=(5, 0))

    
    def display(self, results):
      
        # clear any existing rows
        self.clear()

        # insert per-process rows
        for p in results.get("processes", []):
            self.tree.insert("", "end", values=(
                p.get("pid", ""),
                p.get("arrival", ""),
                p.get("burst", ""),
                p.get("ct", ""),
                p.get("tat", ""),
                p.get("wt", ""),
                p.get("rt", ""),
            ))

        avg_wt = results.get("avg_wt", 0)
        avg_tat = results.get("avg_tat", 0)
        avg_rt = results.get("avg_rt", 0)

        self.avg_label.config(
            text=(
                f"  Avg WT = {avg_wt:.2f}    |    "
                f"Avg TAT = {avg_tat:.2f}    |    "
                f"Avg RT = {avg_rt:.2f}"
            )
        )

    def clear(self):
        # Remove all rows from the table and reset the averages label.
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.avg_label.config(text="")
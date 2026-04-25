import tkinter as tk
from tkinter import ttk

class ResultsTable:

    def __init__(self, root):

        self.tree = ttk.Treeview(
            root,
            columns=("PID","WT","TAT","RT","CT"),
            show="headings"
        )

        for col in ["PID","WT","TAT","RT","CT"]:
            self.tree.heading(col, text=col)

        self.tree.pack()
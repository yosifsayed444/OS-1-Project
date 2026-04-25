import tkinter as tk
from tkinter import messagebox


class MainWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("RR vs SRTF Scheduler")

        self.run_callback = None


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





    def set_run_callback(self, func):

        self.run_callback = func





    def run_clicked(self):

        try:

            quantum = int(self.quantum_entry.get())

            processes = [
                {"pid": "P1", "arrival": 0, "burst": 5},
                {"pid": "P2", "arrival": 1, "burst": 3}
            ]

            if self.run_callback:

                self.run_callback(processes, quantum)

        except:

            messagebox.showerror(
                "Error",
                "Invalid Quantum"
            )





    def show_error(self, msg):

        messagebox.showerror("Error", msg)



    def draw_rr_gantt(self, data):

        print("RR Gantt:", data)



    def draw_srtf_gantt(self, data):

        print("SRTF Gantt:", data)



    def display_rr_results(self, data):

        print("RR Results:", data)



    def display_srtf_results(self, data):

        print("SRTF Results:", data)



    def display_comparison(self, *args):

        print("Comparison:", args)



    def display_conclusion(self, text):

        print("Conclusion:", text)
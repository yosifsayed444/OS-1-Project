import tkinter as tk

class ComparisonPanel:

    def __init__(self, root):

        tk.Label(root,
                 text="Comparison Summary").pack()

        self.text = tk.Text(
            root,
            height=6,
            width=70
        )

        self.text.pack(pady=5)

        tk.Label(root,
                 text="Final Conclusion").pack()

        self.conclusion = tk.Text(
            root,
            height=6,
            width=70
        )

        self.conclusion.pack(pady=5)
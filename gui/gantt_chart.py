import tkinter as tk

class GanttChart:

    def __init__(self, root):

        self.canvas = tk.Canvas(
            root,
            width=600,
            height=80,
            bg="white"
        )

        self.canvas.pack(pady=5)

    def draw(self, blocks):

        x = 10

        for block in blocks:

            width = 40

            self.canvas.create_rectangle(
                x,
                20,
                x + width,
                60
            )

            self.canvas.create_text(
                x + width/2,
                40,
                text=f"P{block.pid}"
            )

            x += width
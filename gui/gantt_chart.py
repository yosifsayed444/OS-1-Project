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

        for process, start, end in blocks:

            width = (end - start) * 40

            self.canvas.create_rectangle(
                x,
                20,
                x + width,
                60,
                fill="lightblue"
            )

            self.canvas.create_text(
                x + width / 2,
                40,
                text=process
            )

            # start time
            self.canvas.create_text(
                x,
                70,
                text=str(start)
            )

            x += width

        # last time
        self.canvas.create_text(
            x,
            70,
            text=str(blocks[-1][2])
        )


#Convert SRTF output to usable format

def convert_srtf(srtf_output):

    if not srtf_output:
        return []

    result = []
    start = srtf_output[0][0]
    current = srtf_output[0][1]

    for i in range(1, len(srtf_output)):
        time, pid = srtf_output[i]

        if pid != current:
            result.append((current, start, time))
            current = pid
            start = time

    result.append((current, start, srtf_output[-1][0] + 1))

    return result
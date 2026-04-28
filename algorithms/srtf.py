class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0


def srtf_scheduling(processes):
    n = len(processes)
    time = 0
    completed = 0
    current_process = None
    gantt_chart = []

    while completed < n:
        available = [p for p in processes if p.arrival_time <= time and p.remaining_time > 0]

        if available:
            shortest = min(available, key=lambda x: x.remaining_time)

            if current_process != shortest:
                current_process = shortest
                gantt_chart.append((time, current_process.pid))

            current_process.remaining_time -= 1
            time += 1

            if current_process.remaining_time == 0:
                completed += 1
                current_process.completion_time = time
        else:
            time += 1

    for p in processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

    return gantt_chart


def print_results(processes, gantt_chart):
    print("\nGantt Chart:")
    for t, pid in gantt_chart:
        print(f"| {pid} ", end="")
    print("|")

    print("\nProcess Details:")
    print("PID\tAT\tBT\tCT\tTAT\tWT")

    total_wt = 0
    total_tat = 0

    for p in processes:
        total_wt += p.waiting_time
        total_tat += p.turnaround_time
        print(f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t{p.completion_time}\t{p.turnaround_time}\t{p.waiting_time}")

    print(f"\nAverage Waiting Time = {total_wt / len(processes):.2f}")
    print(f"Average Turnaround Time = {total_tat / len(processes):.2f}")


if __name__ == "__main__":
    processes = [
        Process("P1", 0, 8),
        Process("P2", 1, 4),
        Process("P3", 2, 2),
        Process("P4", 3, 1)
    ]

    gantt = srtf_scheduling(processes)
    print_results(processes, gantt)
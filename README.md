# Round Robin vs SRTF Comparison Project

A comprehensive tool to analyze and compare Round Robin (RR) and Shortest Remaining Time First (SRTF) CPU scheduling algorithms. This project provides visual insights and performance metrics to evaluate the efficiency of these two fundamental scheduling strategies.

---

## Implementation Technology

- **Programming Language:** Python
- **GUI Technology:** Tkinter

## Repository Structure

```text
project-root/
  src/
    model/       # Process class
    Algorithms/  # Algorithms (Round Robin & SRTF)
    metrics/     # (Waiting Time, Turnaround Time, etc.)
    gui/         # GUI and visualization components
    tests/       # test cases scenarios
  screenshots/   # screenshots for scenarios output
  README.md      # Comprehensive project documentation
  main.py        # Main application entry point
  .gitignore     # Git exclusion rules
```

## Execution Instructions

- **Run:**
  ```bash
  python main.py
  ```

---

## Test Scenarios

The following scenarios are pre-loaded into the application for testing and comparison:

### Scenario A: Basic Workload
- **Description:** A standard set of processes arriving at different times with varied burst lengths.
- **Processes (Arrival, Burst):** (0, 5), (1, 3), (2, 8), (3, 6)

### Scenario B: Quantum Sensitivity
- **Description:** Processes with identical burst times to evaluate how different time quanta affect Round Robin performance.
- **Processes (Arrival, Burst):** (0, 10), (0, 10), (0, 10)

### Scenario C: Short Job Heavy
- **Description:** A long-running process followed by several very short jobs. This highlights how SRTF prevents the "convoy effect."
- **Processes (Arrival, Burst):** (0, 20), (1, 2), (2, 2), (3, 2)

### Scenario D: Interactive Fairness
- **Description:** Multiple processes with identical requirements arriving in sequence to test scheduling fairness.
- **Processes (Arrival, Burst):** (0, 10), (1, 10), (2, 10)

### Scenario E: Validation & Error Handling
- **Description:** A comprehensive suite to verify input sanitization and system robustness.
- **Validations include:**
  - Rejecting non-positive Burst Times.
  - Preventing duplicate Process IDs.
  - Catching missing input values.
  - Flagging invalid (non-numeric or non-positive) Time Quantum values.

---

## Submission Checklist

| Done | Submission Item             | Notes                                                                        |
| :--: | :-------------------------- | :--------------------------------------------------------------------------- |
|  ☐   | **GitHub repository link**  | Must be accessible and point to the final repository.                        |
|  ☐   | **README included**         | Contains project description, requirements, build/run steps, and team names. |
|  ☐   | **Source code included**    | Complete source code must be provided (no compiled-only files).              |
|  ☐   | **Run instructions**        | Detailed steps for execution (Python/IDE setup).                             |
|  ☐   | **Screenshots included**    | UI screenshots and Gantt charts for each algorithm are mandatory.            |
|  ☐   | **Test scenarios**          | At least three documented test scenarios with outputs.                       |
|  ☐   | **Project Submission Form** | Must match the repository and team information exactly.                      |

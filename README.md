# OS-1-Project

# Round Robin vs SRTF Scheduling Project

## 📁 Project Structure

```
Scheduling_Project/
│
├── main.py
│
├── gui/
│   ├── main_window.py        # Main GUI Window
│   ├── input_panel.py       # Process Input Section
│   ├── gantt_chart.py       # Gantt Chart Drawing
│   ├── results_table.py     # Results Tables
│   ├── comparison_panel.py  # Comparison Display
│
├── core/
│   ├── process.py           # Process Class Definition
│   ├── input_validation.py  # Input Checking
│   ├── metrics.py           # WT, TAT, RT Calculations
│
├── algorithms/
│   ├── round_robin.py       # Round Robin Algorithm
│   ├── srtf.py              # SRTF Algorithm
│
├── analysis/
│   ├── comparison.py        # Performance Comparison Logic
│   ├── conclusion.py        # Final Conclusion Generator
│   ├── report_generator.py  # Report Creation
│   ├── test_runner.py       # Run Test Scenarios
│
├── test_cases/
│   ├── scenario_A.txt       # Basic mixed workload
│   ├── scenario_B.txt       # Quantum sensitivity
│   ├── scenario_C.txt       # Short-job-heavy case
│   ├── scenario_D.txt       # Interactive fairness
│   ├── scenario_E.txt       # Validation test
│
└── README.md
```
#  Team Work Distribution (7 Members)

This section describes the responsibilities of each team member and the files assigned to them.

---

##  Member 1 — Input & Validation

 **Responsible for user input and validation**

###  Files:

```
gui/input_panel.py  
core/input_validation.py  
core/process.py  
```

###  Responsibilities:

- Accept number of processes  
- Accept:
  - Process ID  
  - Arrival Time  
  - Burst Time  
- Accept Quantum value  
- Prevent invalid inputs  
- Display error messages  

###  Covers Requirements:

- Accept dynamic number of processes  
- Validate all input  
- Reject invalid quantum values safely  

---

##  Member 2 — Round Robin Algorithm

🎯 **Responsible for full Round Robin implementation**

###  Files:

```
algorithms/round_robin.py  
gui/ready_queue_view.py  
```

###  Responsibilities:

- Implement Round Robin scheduling  
- Use Time Quantum  
- Manage Ready Queue  
- Generate Gantt Chart data  

###  Covers Requirements:

- Simulate Round Robin correctly  
- Ready Queue View  
- Time Quantum behavior  

---

##  Member 3 — SRTF Algorithm

  **Responsible for SRTF implementation**

###  Files:

```
algorithms/srtf.py  
```

###  Responsibilities:

- Implement Shortest Remaining Time First  
- Handle Preemption  
- Select process with shortest remaining time  

###  Covers Requirements:

- Simulate SRTF correctly  
- Immediate Preemption  

---

##  Member 4 — Metrics Calculation

🎯 **Responsible for performance calculations**

###  Files:

```
core/metrics.py  
gui/results_table.py  
```

###  Responsibilities:

Calculate:

- Waiting Time (WT)  
- Turnaround Time (TAT)  
- Response Time (RT)  
- Average WT  
- Average TAT  
- Average RT  

Display results in tables.

###  Covers Requirements:

- Calculate WT  
- Calculate TAT  
- Calculate RT  
- Display Results Tables  

---

##  Member 5 — Gantt Charts

**Responsible for visualization**

###  Files:

```
gui/gantt_chart.py  
```

###  Responsibilities:

Draw:

- Round Robin Gantt Chart  
- SRTF Gantt Chart  

###  Covers Requirements:

- Display separate Gantt charts  

---

##  Member 6 — Comparison & Analysis

 **Responsible for algorithm comparison**

###  Files:

```
analysis/comparison.py  
gui/comparison_panel.py  
```

###  Responsibilities:

Compare:

- Fairness vs Efficiency  
- Response Time  
- Waiting Time  
- Short Job Performance  
- Quantum Effect  

Answer analysis questions such as:

- Which algorithm gave better average waiting time?  
- Which algorithm gave better response time?  
- Did Round Robin appear fairer?  
- Did SRTF complete short jobs faster?  

###  Covers Requirements:

- Required Comparison Focus  
- Required Analysis Questions  

---

##  Member 7 — Conclusion & Testing

🎯 **Responsible for final output and testing**

###  Files:

```
analysis/conclusion.py  
analysis/test_runner.py  
analysis/report_generator.py  
test_cases/  
```

### Responsibilities:

- Write Final Conclusion  
- Run Test Scenarios  
- Generate Report  
- Prepare test inputs  

###  Test Scenarios:

- Scenario A — Basic mixed workload  
- Scenario B — Quantum sensitivity  
- Scenario C — Short-job-heavy case  
- Scenario D — Interactive fairness  
- Scenario E — Validation case  

###  Covers Requirements:

- Required Conclusion  
- Required Test Scenarios  

---

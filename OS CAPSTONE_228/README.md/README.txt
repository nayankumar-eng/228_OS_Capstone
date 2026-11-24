# OS Resource Manager

## Integrated Python + Bash Operating System Resource Management Simulator

---

## 1. Project Description

OS Resource Manager is an integrated application that simulates major operating-system resource-management functions.

The application combines Python algorithms with Bash system-level information.

---

## 2. Features

The application provides:

- CPU Scheduling
- Memory Management
- Deadlock Detection
- Disk Scheduling
- Bash System Monitoring
- Performance Analysis
- CSV Report Generation
- Activity Logging
- Input Validation
- Exception Handling

---

## 3. CPU Scheduling

Algorithms:

1. FCFS
2. SJF
3. Round Robin

Metrics:

- Completion Time
- Waiting Time
- Turnaround Time

---

## 4. Memory Management

Algorithms:

1. First Fit
2. Best Fit
3. Worst Fit

---

## 5. Deadlock Management

Algorithm:

Banker's Algorithm

Output:

- Need Matrix
- Safe State
- Unsafe State
- Safe Sequence

---

## 6. Disk Scheduling

Algorithms:

1. FCFS
2. SSTF

Metric:

Total Disk Head Movement

---

## 7. Bash Integration

The Python program executes:

scripts/system_info.sh

The Bash script displays:

- Operating System
- Kernel
- Architecture
- Hostname
- Python Version
- Date
- Memory
- Disk information

---

## 8. Requirements

Python 3.9 or later.

Bash shell.

Linux, macOS, WSL or Git Bash is recommended.

No third-party Python packages are required.

---

## 9. Project Structure

```text
OS_Resource_Manager_Project/
│
├── src/
│   └── os_resource_manager.py
│
├── scripts/
│   └── system_info.sh
│
├── data/
│
├── logs/
│   └── activity.log
│
├── reports/
│   ├── concise_report.md
│   ├── test_cases.md
│   ├── sample_output.txt
│   ├── analysis_report.txt
│   ├── cpu_comparison.csv
│   ├── memory_comparison.csv
│   └── disk_comparison.csv
│
├── screenshots/
│
├── README.md
│
└── demo.sh

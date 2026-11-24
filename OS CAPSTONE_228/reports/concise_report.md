# OS Resource Manager — Project Report

## 1. Introduction

OS Resource Manager is an integrated Python-and-Bash application designed to simulate major operating-system resource-management functions.

The application provides CPU scheduling, memory allocation, deadlock detection, disk scheduling, system monitoring and performance analysis through a single menu-driven interface.

The project demonstrates how different operating-system algorithms can be integrated into one software system.

---

## 2. Objectives

The main objectives are:

1. Simulate CPU scheduling algorithms.
2. Simulate memory allocation algorithms.
3. Detect safe and unsafe states using Banker's Algorithm.
4. Simulate disk scheduling algorithms.
5. Integrate Python with Bash.
6. Compare algorithm performance.
7. Generate analytical reports.
8. Validate user input.
9. Maintain activity logs.
10. Provide a complete integrated OS simulation application.

---

# Phase 1 — System Design and Planning

## Architecture

The application follows this flow:

User
↓
Main Menu
↓
Input Validation
↓
Selected OS Module
↓
Algorithm Execution
↓
Performance Calculation
↓
Result Display
↓
Logging / Reporting

## Modules

The application contains:

- CPU Scheduling
- Memory Management
- Deadlock Management
- Disk Scheduling
- Bash System Monitoring
- Reporting
- Logging

## Data Structures

Lists are used for:

- Burst times
- Memory blocks
- Process sizes
- Disk requests

Matrices are used for:

- MAX matrix
- ALLOCATION matrix
- NEED matrix

Dictionaries are used for performance metrics.

---

# Phase 2 — Core Resource-Management Modules

## CPU Scheduling

Implemented algorithms:

- FCFS
- SJF
- Round Robin

Metrics:

- Waiting time
- Turnaround time
- Completion time

## Memory Management

Implemented algorithms:

- First Fit
- Best Fit
- Worst Fit

## Deadlock

Banker's Algorithm is implemented to determine:

- Safe state
- Unsafe state
- Safe sequence
- Need matrix

## Storage

Implemented disk scheduling:

- FCFS
- SSTF

Metric:

- Total disk-head movement

## Bash Integration

The Python application executes:

system_info.sh

using the subprocess module.

The Bash script displays:

- Operating system
- Kernel
- Architecture
- Hostname
- Python version
- Date
- Memory information
- Disk information

---

# Phase 3 — Analysis and Comparison

Algorithms are tested using common datasets.

CPU metrics:

- Average waiting time
- Average turnaround time

Memory metrics:

- Allocation
- Remaining memory

Disk metrics:

- Total head movement

Deadlock metric:

- Safe/unsafe state
- Safe sequence

The application generates CSV files for comparison.

---

# Phase 4 — Testing and Reliability

Testing includes:

- Valid input
- Invalid input
- Negative input
- Non-numeric input
- Zero quantum
- Invalid menu selection
- Invalid Banker's matrix
- Allocation greater than maximum claim
- Boundary cases

Exception handling prevents the program from crashing because of normal user input errors.

Activity logging records important operations.

---

# Phase 5 — Documentation and Demonstration

The project contains:

- Source code
- Bash script
- README
- Test cases
- Sample output
- Analysis reports
- CSV comparison tables
- Screenshots
- Activity logs

The application can be demonstrated using the main menu.

---

# Conclusion

The OS Resource Manager successfully integrates major operating-system resource-management algorithms into one application.

Python provides the main algorithmic implementation and reporting system, while Bash provides operating-system level information.

The modular design allows future extensions such as paging, synchronization, additional CPU scheduling algorithms and graphical visualization.

import os
import csv
import subprocess
from pathlib import Path
from collections import deque


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"
SCRIPT_DIR = BASE_DIR / "scripts"

LOG_FILE = LOG_DIR / "activity.log"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)
SCRIPT_DIR.mkdir(exist_ok=True)


# ============================================================
# LOGGING
# ============================================================

def log_activity(message):
    """Store project activity in the log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{message}\n")


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_numbers(values, name="values"):
    """Validate that all values are non-negative integers."""

    try:
        numbers = [int(x) for x in values]

        if any(number < 0 for number in numbers):
            raise ValueError(f"{name} cannot contain negative values.")

        return numbers

    except ValueError:
        raise ValueError(f"{name} must contain valid integers.")


# ============================================================
# CPU SCHEDULING
# ============================================================

def fcfs(burst_times):
    """First Come First Serve scheduling."""

    waiting = [0] * len(burst_times)
    turnaround = [0] * len(burst_times)

    for i in range(1, len(burst_times)):
        waiting[i] = waiting[i - 1] + burst_times[i - 1]

    for i in range(len(burst_times)):
        turnaround[i] = waiting[i] + burst_times[i]

    return waiting, turnaround


def sjf(burst_times):
    """Non-preemptive Shortest Job First."""

    processes = list(enumerate(burst_times))
    processes.sort(key=lambda x: x[1])

    waiting = [0] * len(burst_times)
    turnaround = [0] * len(burst_times)

    current_time = 0

    for process_id, burst in processes:
        waiting[process_id] = current_time
        turnaround[process_id] = current_time + burst
        current_time += burst

    return waiting, turnaround


def round_robin(burst_times, quantum):
    """Round Robin CPU scheduling."""

    n = len(burst_times)

    remaining = burst_times.copy()
    waiting = [0] * n
    turnaround = [0] * n

    queue = deque(range(n))
    current_time = 0

    while queue:

        process = queue.popleft()

        execution_time = min(quantum, remaining[process])

        current_time += execution_time
        remaining[process] -= execution_time

        for i in range(n):
            if i != process and remaining[i] > 0:
                waiting[i] += execution_time

        if remaining[process] > 0:
            queue.append(process)
        else:
            turnaround[process] = current_time

    for i in range(n):
        waiting[i] = turnaround[i] - burst_times[i]

    return waiting, turnaround


def calculate_metrics(waiting, turnaround):
    """Calculate average waiting and turnaround time."""

    avg_waiting = sum(waiting) / len(waiting)
    avg_turnaround = sum(turnaround) / len(turnaround)

    return avg_waiting, avg_turnaround


def display_cpu_results(name, waiting, turnaround):

    avg_waiting, avg_turnaround = calculate_metrics(
        waiting,
        turnaround
    )

    print("\n----------------------------------------")
    print(name)
    print("----------------------------------------")

    print("Waiting Time:", waiting)
    print("Turnaround Time:", turnaround)

    print(f"Average Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")

    return avg_waiting, avg_turnaround


def cpu_scheduling():

    print("\n========================================")
    print("          CPU SCHEDULING")
    print("========================================")

    try:

        burst_input = input(
            "Enter burst times separated by spaces: "
        )

        burst_times = validate_numbers(
            burst_input.split(),
            "Burst times"
        )

        if len(burst_times) == 0:
            raise ValueError("At least one process is required.")

        quantum = int(
            input("Enter Round Robin quantum: ")
        )

        if quantum <= 0:
            raise ValueError("Quantum must be greater than zero.")

        print("\nProcesses:", len(burst_times))
        print("Burst Times:", burst_times)

        fcfs_waiting, fcfs_turnaround = fcfs(
            burst_times
        )

        sjf_waiting, sjf_turnaround = sjf(
            burst_times
        )

        rr_waiting, rr_turnaround = round_robin(
            burst_times,
            quantum
        )

        fcfs_avg_w, fcfs_avg_t = display_cpu_results(
            "FCFS",
            fcfs_waiting,
            fcfs_turnaround
        )

        sjf_avg_w, sjf_avg_t = display_cpu_results(
            "SJF",
            sjf_waiting,
            sjf_turnaround
        )

        rr_avg_w, rr_avg_t = display_cpu_results(
            "Round Robin",
            rr_waiting,
            rr_turnaround
        )

        log_activity(
            "CPU Scheduling executed successfully."
        )

        return {
            "FCFS": (fcfs_avg_w, fcfs_avg_t),
            "SJF": (sjf_avg_w, sjf_avg_t),
            "Round Robin": (rr_avg_w, rr_avg_t)
        }

    except Exception as error:

        print(f"\nError: {error}")

        log_activity(
            f"CPU Scheduling Error: {error}"
        )


# ============================================================
# MEMORY MANAGEMENT
# ============================================================

def first_fit(blocks, processes):

    allocation = [-1] * len(processes)

    available = blocks.copy()

    for i, process in enumerate(processes):

        for j in range(len(available)):

            if available[j] >= process:

                allocation[i] = j
                available[j] -= process
                break

    return allocation


def best_fit(blocks, processes):

    allocation = [-1] * len(processes)

    available = blocks.copy()

    for i, process in enumerate(processes):

        best_index = -1

        for j in range(len(available)):

            if available[j] >= process:

                if (
                    best_index == -1
                    or available[j] < available[best_index]
                ):
                    best_index = j

        if best_index != -1:

            allocation[i] = best_index
            available[best_index] -= process

    return allocation


def worst_fit(blocks, processes):

    allocation = [-1] * len(processes)

    available = blocks.copy()

    for i, process in enumerate(processes):

        worst_index = -1

        for j in range(len(available)):

            if available[j] >= process:

                if (
                    worst_index == -1
                    or available[j] > available[worst_index]
                ):
                    worst_index = j

        if worst_index != -1:

            allocation[i] = worst_index
            available[worst_index] -= process

    return allocation


def display_memory_result(name, allocation, processes):

    print("\n----------------------------------------")
    print(name)
    print("----------------------------------------")

    for i, block in enumerate(allocation):

        if block != -1:

            print(
                f"Process {i + 1} "
                f"({processes[i]}) -> "
                f"Block {block + 1}"
            )

        else:

            print(
                f"Process {i + 1} "
                f"({processes[i]}) -> "
                f"Not Allocated"
            )


def memory_management():

    print("\n========================================")
    print("          MEMORY MANAGEMENT")
    print("========================================")

    try:

        blocks_input = input(
            "Enter memory block sizes: "
        )

        process_input = input(
            "Enter process sizes: "
        )

        blocks = validate_numbers(
            blocks_input.split(),
            "Memory blocks"
        )

        processes = validate_numbers(
            process_input.split(),
            "Process sizes"
        )

        if not blocks or not processes:
            raise ValueError(
                "Blocks and processes cannot be empty."
            )

        ff = first_fit(blocks, processes)
        bf = best_fit(blocks, processes)
        wf = worst_fit(blocks, processes)

        print("\nMemory Blocks:", blocks)
        print("Processes:", processes)

        display_memory_result(
            "First Fit",
            ff,
            processes
        )

        display_memory_result(
            "Best Fit",
            bf,
            processes
        )

        display_memory_result(
            "Worst Fit",
            wf,
            processes
        )

        log_activity(
            "Memory Management executed successfully."
        )

    except Exception as error:

        print(f"\nError: {error}")

        log_activity(
            f"Memory Management Error: {error}"
        )


# ============================================================
# BANKER'S ALGORITHM
# ============================================================

def bankers_algorithm(
    allocation,
    maximum,
    available
):

    processes = len(allocation)
    resources = len(available)

    need = []

    for i in range(processes):

        row = []

        for j in range(resources):

            row.append(
                maximum[i][j] -
                allocation[i][j]
            )

        need.append(row)

    work = available.copy()

    finish = [False] * processes

    safe_sequence = []

    while len(safe_sequence) < processes:

        found = False

        for i in range(processes):

            if not finish[i]:

                possible = True

                for j in range(resources):

                    if need[i][j] > work[j]:

                        possible = False
                        break

                if possible:

                    for j in range(resources):

                        work[j] += allocation[i][j]

                    finish[i] = True
                    safe_sequence.append(i)

                    found = True

        if not found:
            return False, safe_sequence, need

    return True, safe_sequence, need


def deadlock_management():

    print("\n========================================")
    print("       DEADLOCK DETECTION")
    print("========================================")

    try:

        processes = int(
            input("Enter number of processes: ")
        )

        resources = int(
            input("Enter number of resources: ")
        )

        if processes <= 0 or resources <= 0:
            raise ValueError(
                "Number of processes/resources must be positive."
            )

        print("\nEnter Available Resources:")

        available = validate_numbers(
            input().split(),
            "Available resources"
        )

        if len(available) != resources:
            raise ValueError(
                "Available resources count does not match."
            )

        print("\nEnter Allocation Matrix:")

        allocation = []

        for i in range(processes):

            row = validate_numbers(
                input(f"P{i}: ").split(),
                f"Allocation row {i}"
            )

            if len(row) != resources:
                raise ValueError(
                    "Allocation row size mismatch."
                )

            allocation.append(row)

        print("\nEnter Maximum Matrix:")

        maximum = []

        for i in range(processes):

            row = validate_numbers(
                input(f"P{i}: ").split(),
                f"Maximum row {i}"
            )

            if len(row) != resources:
                raise ValueError(
                    "Maximum row size mismatch."
                )

            maximum.append(row)

        safe, sequence, need = bankers_algorithm(
            allocation,
            maximum,
            available
        )

        print("\nNeed Matrix:")

        for i, row in enumerate(need):

            print(f"P{i}: {row}")

        if safe:

            sequence_text = " -> ".join(
                f"P{i}" for i in sequence
            )

            print("\nSystem is in SAFE STATE.")
            print("Safe Sequence:", sequence_text)

        else:

            print("\nSystem is NOT in a safe state.")
            print("Possible partial sequence:", sequence)

        log_activity(
            "Banker's Algorithm executed successfully."
        )

    except Exception as error:

        print(f"\nError: {error}")

        log_activity(
            f"Deadlock Detection Error: {error}"
        )


# ============================================================
# DISK SCHEDULING
# ============================================================

def disk_fcfs(requests, head):

    movement = 0
    current = head

    order = []

    for request in requests:

        movement += abs(
            current - request
        )

        current = request
        order.append(request)

    return movement, order


def disk_sstf(requests, head):

    remaining = requests.copy()

    current = head

    movement = 0

    order = []

    while remaining:

        closest = min(
            remaining,
            key=lambda x: abs(x - current)
        )

        movement += abs(
            current - closest
        )

        current = closest

        order.append(closest)

        remaining.remove(closest)

    return movement, order


def disk_scheduling():

    print("\n========================================")
    print("          DISK SCHEDULING")
    print("========================================")

    try:

        head = int(
            input("Enter initial head position: ")
        )

        requests = validate_numbers(
            input(
                "Enter disk requests: "
            ).split(),
            "Disk requests"
        )

        if not requests:
            raise ValueError(
                "At least one disk request is required."
            )

        fcfs_movement, fcfs_order = disk_fcfs(
            requests,
            head
        )

        sstf_movement, sstf_order = disk_sstf(
            requests,
            head
        )

        print("\nFCFS")
        print("Order:", fcfs_order)
        print("Total Head Movement:", fcfs_movement)

        print("\nSSTF")
        print("Order:", sstf_order)
        print("Total Head Movement:", sstf_movement)

        log_activity(
            "Disk Scheduling executed successfully."
        )

    except Exception as error:

        print(f"\nError: {error}")

        log_activity(
            f"Disk Scheduling Error: {error}"
        )


# ============================================================
# BASH INTEGRATION
# ============================================================

def run_bash_script():

    print("\n========================================")
    print("       BASH SYSTEM MONITOR")
    print("========================================")

    script_path = SCRIPT_DIR / "system_info.sh"

    if not script_path.exists():

        print("Bash script not found.")

        log_activity(
            "Bash script not found."
        )

        return

    try:

        result = subprocess.run(
            ["bash", str(script_path)],
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.stderr:

            print("Bash Error:")
            print(result.stderr)

        log_activity(
            "Bash system information executed."
        )

    except Exception as error:

        print(f"\nError running Bash script: {error}")

        log_activity(
            f"Bash Integration Error: {error}"
        )


# ============================================================
# CSV REPORT
# ============================================================

def write_csv(filename, headers, rows):

    file_path = REPORT_DIR / filename

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(headers)

        writer.writerows(rows)


# ============================================================
# REPORT GENERATION
# ============================================================

def generate_reports():

    print("\n========================================")
    print("       GENERATING REPORTS")
    print("========================================")

    # Common CPU dataset

    burst_times = [8, 4, 9, 5, 2]
    quantum = 3

    fcfs_w, fcfs_t = fcfs(
        burst_times
    )

    sjf_w, sjf_t = sjf(
        burst_times
    )

    rr_w, rr_t = round_robin(
        burst_times,
        quantum
    )

    fcfs_avg_w, fcfs_avg_t = calculate_metrics(
        fcfs_w,
        fcfs_t
    )

    sjf_avg_w, sjf_avg_t = calculate_metrics(
        sjf_w,
        sjf_t
    )

    rr_avg_w, rr_avg_t = calculate_metrics(
        rr_w,
        rr_t
    )

    write_csv(
        "cpu_comparison.csv",
        [
            "Algorithm",
            "Average Waiting Time",
            "Average Turnaround Time"
        ],
        [
            ["FCFS", fcfs_avg_w, fcfs_avg_t],
            ["SJF", sjf_avg_w, sjf_avg_t],
            ["Round Robin", rr_avg_w, rr_avg_t]
        ]
    )

    # Memory dataset

    blocks = [100, 500, 200, 300, 600]
    processes = [212, 417, 112, 426]

    ff = first_fit(blocks, processes)
    bf = best_fit(blocks, processes)
    wf = worst_fit(blocks, processes)

    ff_allocated = sum(
        1 for x in ff if x != -1
    )

    bf_allocated = sum(
        1 for x in bf if x != -1
    )

    wf_allocated = sum(
        1 for x in wf if x != -1
    )

    write_csv(
        "memory_comparison.csv",
        [
            "Algorithm",
            "Processes Allocated"
        ],
        [
            ["First Fit", ff_allocated],
            ["Best Fit", bf_allocated],
            ["Worst Fit", wf_allocated]
        ]
    )

    # Disk dataset

    head = 53
    requests = [
        98,
        183,
        37,
        122,
        14,
        124,
        65,
        67
    ]

    fcfs_movement, _ = disk_fcfs(
        requests,
        head
    )

    sstf_movement, _ = disk_sstf(
        requests,
        head
    )

    write_csv(
        "disk_comparison.csv",
        [
            "Algorithm",
            "Total Head Movement"
        ],
        [
            ["FCFS", fcfs_movement],
            ["SSTF", sstf_movement]
        ]
    )

    # Analysis report

    analysis_file = REPORT_DIR / "analysis_report.txt"

    with open(
        analysis_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "OS RESOURCE MANAGER - ANALYSIS REPORT\n"
        )

        file.write(
            "=====================================\n\n"
        )

        file.write(
            "CPU Scheduling Comparison\n"
        )

        file.write(
            f"FCFS Average Waiting Time: "
            f"{fcfs_avg_w:.2f}\n"
        )

        file.write(
            f"SJF Average Waiting Time: "
            f"{sjf_avg_w:.2f}\n"
        )

        file.write(
            f"Round Robin Average Waiting Time: "
            f"{rr_avg_w:.2f}\n\n"
        )

        file.write(
            "Memory Management Comparison\n"
        )

        file.write(
            f"First Fit Allocated Processes: "
            f"{ff_allocated}\n"
        )

        file.write(
            f"Best Fit Allocated Processes: "
            f"{bf_allocated}\n"
        )

        file.write(
            f"Worst Fit Allocated Processes: "
            f"{wf_allocated}\n\n"
        )

        file.write(
            "Disk Scheduling Comparison\n"
        )

        file.write(
            f"FCFS Total Head Movement: "
            f"{fcfs_movement}\n"
        )

        file.write(
            f"SSTF Total Head Movement: "
            f"{sstf_movement}\n"
        )

        file.write(
            "\nObservations\n"
        )

        file.write(
            "1. SJF generally reduces average waiting time "
            "when short processes are available.\n"
        )

        file.write(
            "2. Round Robin provides fair CPU time sharing "
            "among processes.\n"
        )

        file.write(
            "3. Memory allocation algorithms differ in "
            "how they use available memory blocks.\n"
        )

        file.write(
            "4. SSTF can reduce disk head movement compared "
            "with simple FCFS for this dataset.\n"
        )

    print("\nReports generated successfully.")

    print(
        "Location:",
        REPORT_DIR
    )

    log_activity(
        "Analysis reports generated successfully."
    )


# ============================================================
# MAIN MENU
# ============================================================

def main():

    print("\n========================================")
    print("        OS RESOURCE MANAGER")
    print("========================================")

    print(
        "Integrated CPU, Memory, Deadlock, "
        "Disk and Bash Resource Manager"
    )

    while True:

        print("\n----------------------------------------")
        print("MAIN MENU")
        print("----------------------------------------")

        print("1. CPU Scheduling")
        print("2. Memory Management")
        print("3. Deadlock Detection")
        print("4. Disk Scheduling")
        print("5. Run Bash System Monitor")
        print("6. Generate Analysis Reports")
        print("0. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            cpu_scheduling()

        elif choice == "2":

            memory_management()

        elif choice == "3":

            deadlock_management()

        elif choice == "4":

            disk_scheduling()

        elif choice == "5":

            run_bash_script()

        elif choice == "6":

            generate_reports()

        elif choice == "0":

            print(
                "\nThank you for using "
                "OS Resource Manager."
            )

            log_activity(
                "Application exited."
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 0-6."
            )

            log_activity(
                f"Invalid menu choice: {choice}"
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()
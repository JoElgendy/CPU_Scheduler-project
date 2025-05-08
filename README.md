# 🧠 CPU Scheduler Simulator

**Faculty of Engineering, Ain Shams University – Operating Systems Project (CSE335s)**  
A desktop GUI application that simulates various CPU scheduling algorithms in both live and static modes. Developed as a group project to visualize the inner workings of OS process scheduling.

## 📌 Overview

This project presents a real-time CPU Scheduler simulator that helps students understand and visualize how different scheduling algorithms function. With a user-friendly GUI, dynamic Gantt chart, and live simulation capabilities, users can interactively explore each algorithm’s behavior.

## 🎯 Features

- ✅ **Supports Multiple Scheduling Algorithms**:
  - First Come First Served (FCFS)
  - Shortest Job First (SJF) – Preemptive & Non-Preemptive
  - Priority Scheduling – Preemptive & Non-Preemptive
  - Round Robin

- 📊 **Two Execution Modes**:
  - **Static Mode**: Calculates results and displays final Gantt chart immediately.
  - **Live Mode**: Real-time step-by-step simulation (1 time unit = 1 second), with dynamic Gantt chart updates.

- 🔁 **Dynamic Process Management**:
  - Add new processes during live execution.
  - Interactive input for arrival time, burst time, priority, and quantum (if applicable).

- 📈 **Real-Time Metrics**:
  - Gantt Chart
  - Average Waiting Time
  - Average Turnaround Time
  - Remaining Burst Times Table

## 🖥 GUI Highlights

- Dropdown menu to select scheduling algorithm.
- Inputs for:
  - Number of processes
  - Time quantum (Round Robin only)
  - Arrival time, burst time, priority
- Gantt chart canvas that updates live.
- Buttons to start/stop simulation.
- Process table displaying real-time updates.

## ⚙️ Technologies Used

- **Language**: Python  
- **GUI Library**: Tkinter  
- **OS Compatibility**: Windows  

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/JoElgendy/CPU_Scheduler-project
   cd CPU_Scheduler-project
   ```
2. Make sure Python is installed.
3. Run the main file:
   ```bash
   python main.py
   ```

Or download the executable:  
👉 [Download CPU_Scheduler.exe](https://drive.google.com/file/d/1F_-IA4H8k75-u5N9ZaOFnplq_7blYl0u/view?usp=sharing)

## 🧑‍💻 Team Members

| Name                          | ID        |
|-------------------------------|-----------|
| Yousef Sherif Ali Hassan      | 2101118   |
| Adham Nasreldin Mahmoud       | 2101137   |
| Ali Mahmoud El-Sayed          | 2101751   |
| Yousef Mohammed H. Abouelela  | 2101076   |
| Youssof Waleed Fathi Hassan   | 2101734   |
| Marwan Osama Salama Aboelsoud | 2100769   |
| Ehab Ahmed Abdelhamid         | 2100632   |

## 📚 License

This project is developed for educational purposes. You are free to use and modify it with attribution.

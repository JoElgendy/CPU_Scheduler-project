import tkinter as tk
from tkinter import ttk, messagebox

class CPU_Scheduler_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduler")
        self.root.geometry("500x400")

        # Frame for Scheduler Type Section
        self.scheduler_section = tk.Frame(root)
        self.scheduler_section.pack(pady=10)

        tk.Label(self.scheduler_section, text="Select Scheduler Type:").pack()

        self.scheduler_type_var = tk.StringVar()
        self.scheduler_dropdown = ttk.Combobox(
            self.scheduler_section,
            textvariable=self.scheduler_type_var,
            values=("FCFS", "SJF Preemptive", "SJF non_Preemptive", "Priority Preemptive", "Priority non_Preemptive", "Round Robin"),
            state="readonly",
            width=50
        )
        self.scheduler_dropdown.pack(pady=5)
        self.scheduler_dropdown.bind("<<ComboboxSelected>>", self.set_scheduler_type)

        # Quantum input 
        self.quantum_frame = tk.Frame(self.scheduler_section)
        self.quantum_label = tk.Label(self.quantum_frame, text="Enter Quantum:")
        self.quantum_entry = tk.Entry(self.quantum_frame, font=("Arial", 14))

        self.quantum_frame.pack_forget()

        # Priority Field (optional)
        self.priority_frame = tk.Frame(self.scheduler_section)
        self.priority_label = tk.Label(self.priority_frame, text="Enter Priority:")
        self.priority_entry = tk.Entry(self.priority_frame)

        self.priority_frame.pack_forget()

        # Burst time Field (always visible)
        self.burst_time_frame = tk.Frame(self.scheduler_section)
        self.burst_time_label = tk.Label(self.burst_time_frame, text="Enter Burst Time:")  
        self.burst_time_entry = tk.Entry(self.burst_time_frame, font=("Arial", 14), width=20)  
        self.burst_time_label.pack(side="left")
        self.burst_time_entry.pack(side="left", padx=5)
        self.burst_time_frame.pack(pady=5) 

        # Gantt Chart
        self.gantt_chart_label = tk.Label(root, text="Gantt Chart:")
        self.gantt_chart_label.pack(pady=10)

        # Start and Add buttons (to be packed conditionally)
        self.start_button = tk.Button(self.scheduler_section, text="Start Scheduler", command=self.start_scheduler)
        self.add_process_button = tk.Button(self.scheduler_section, text="Add Process", command=self.add_process)

    def set_scheduler_type(self, event=None):
        scheduler = self.scheduler_type_var.get()

        # Hide all fields first
        self.quantum_frame.pack_forget()
        self.priority_frame.pack_forget()
        self.start_button.pack_forget()
        self.add_process_button.pack_forget()
        

        if scheduler == "Round Robin":
            self.quantum_label.pack(side="left")
            self.quantum_entry.pack(side="left", padx=5)
            self.quantum_frame.pack(pady=5)
        elif scheduler == "Priority Preemptive" or scheduler == "Priority non_Preemptive":
            self.priority_label.pack(side="left")
            self.priority_entry.pack(side="left", padx=5)
            self.priority_frame.pack(pady=5)

        # Pack the buttons after the relevant fields
        self.add_process_button.pack(pady=10)
        self.start_button.pack(pady=10)
        

    def start_scheduler(self):
        scheduler = self.scheduler_type_var.get()
        if not scheduler:
            messagebox.showerror("Error", "Please select a scheduler type.")
            return

        if scheduler == "Round Robin":
            quantum = self.quantum_entry.get()
            if not quantum:
                messagebox.showerror("Error", "Please enter a quantum value.")
                return

        if scheduler == "Priority Preemptive" or scheduler == "Priority non_Preemptive":
            priority = self.priority_entry.get()
            if not priority:
                messagebox.showerror("Error", "Please enter a priority value.")
                return

        # Get Burst Time input
        burst_time = self.burst_time_entry.get()
        if not burst_time:
            messagebox.showerror("Error", "Please enter a burst time value.")
            return

        self.gantt_chart_label.config(text=f"Gantt Chart: [{scheduler}]")  # Placeholder

    def add_process(self):
        messagebox.showinfo("Add Process", "Process added successfully!")  # Placeholder for the "Add Process" functionality

if __name__ == "__main__":
    root = tk.Tk()
    app = CPU_Scheduler_GUI(root)
    root.mainloop()

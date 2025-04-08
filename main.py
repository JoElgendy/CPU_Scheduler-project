import tkinter as tk
from tkinter import ttk, messagebox


class CPU_Scheduler_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduler")
        self.root.geometry("600x600")

        # Apply styling to the window
        self.root.config(bg="#f0f0f0")

        # Create a Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        # Create Frames for Tabs
        self.scheduler_frame = ttk.Frame(self.notebook, padding=(0, 10, 0, 10))
        self.notebook.add(self.scheduler_frame, text="Scheduler Settings")

        self.process_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.process_frame, text="Process Entry")

        scheduler_frame_inner_grid = ttk.Frame(self.scheduler_frame)

        # Scheduler Type Dropdown (first page)
        self.scheduler_type_var = tk.StringVar()
        self.scheduler_type_label = ttk.Label(
            scheduler_frame_inner_grid,
            text="Select Scheduler Type:",
            font=("Arial", 12),
        )
        self.scheduler_type_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.scheduler_dropdown = ttk.Combobox(
            scheduler_frame_inner_grid,
            textvariable=self.scheduler_type_var,
            values=(
                "FCFS",
                "SJF Preemptive",
                "SJF non_Preemptive",
                "Priority Preemptive",
                "Priority non_Preemptive",
                "Round Robin",
            ),
            state="readonly",
        )
        self.scheduler_dropdown.grid(row=0, column=1, pady=5)

        # Number of Processes Field
        self.num_process_label = ttk.Label(
            scheduler_frame_inner_grid,
            text="Enter Number of Processes:",
            font=("Arial", 12),
        )
        self.num_process_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.num_process_entry = ttk.Entry(
            scheduler_frame_inner_grid, font=("Arial", 12), width=20
        )
        self.num_process_entry.grid(row=1, column=1, pady=5, sticky="ew")

        scheduler_frame_inner_grid.pack()

        # Next button to move to process entry page
        self.next_button = ttk.Button(
            self.scheduler_frame,
            text="Confirm",
            command=self.show_process_page,
            width=20,
        )
        self.next_button.pack(pady=10)

        # Frame for entering processes
        self.process_label = ttk.Label(
            self.process_frame, text="Enter Processes Data", font=("Arial", 14)
        )
        self.process_label.pack(pady=10)

        # Hide the process entry page initially
        self.process_frame.pack_forget()

        # List to store process data (e.g., [burst_time, priority, arrival_time])
        self.processes = []

        # Fields for Priority and Quantum (these will be used conditionally)
        self.priority_frame = None
        self.quantum_frame = None

    def show_process_page(self):
        # Move to process entry page after selecting scheduler type
        scheduler = self.scheduler_type_var.get()

        try:
            num_processes = int(self.num_process_entry.get())
            if num_processes <= 0:
                raise ValueError("Number of processes must be a positive integer.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            return

        if not scheduler:
            messagebox.showerror("Error", "Please select a scheduler type.")
            return

        # Reset process page in case user changed his mind about any of first frame input values
        for widget in self.process_frame.winfo_children():
            widget.destroy()

        # Dynamically create entry fields for each process
        self.processes = []  # Reset process data
        for i in range(num_processes):
            process_frame = ttk.Frame(self.process_frame)
            process_frame.pack(pady=5)

            # Arrival Time Field (always displayed)
            arrival_time_label = ttk.Label(
                process_frame,
                text=f"Arrival Time for Process {i+1}:",
                font=("Arial", 12),
            )
            arrival_time_label.grid(row=0, column=0, padx=5, sticky="e")

            arrival_time_entry = ttk.Entry(process_frame, font=("Arial", 12), width=10)
            arrival_time_entry.grid(row=0, column=1, padx=5)

            # Burst Time Field (always displayed)
            burst_time_label = ttk.Label(
                process_frame, text=f"Burst Time for Process {i+1}:", font=("Arial", 12)
            )
            burst_time_label.grid(row=1, column=0, padx=5, sticky="e")

            burst_time_entry = ttk.Entry(process_frame, font=("Arial", 12), width=10)
            burst_time_entry.grid(row=1, column=1, padx=5)

            # Priority Field (only displayed if needed)
            if self.scheduler_type_var.get() in [
                "Priority Preemptive",
                "Priority non_Preemptive",
            ]:
                priority_label = ttk.Label(
                    process_frame,
                    text=f"Priority for Process {i+1}:",
                    font=("Arial", 12),
                )
                priority_label.grid(row=2, column=0, padx=5, sticky="e")

                priority_entry = ttk.Entry(process_frame, font=("Arial", 12), width=10)
                priority_entry.grid(row=2, column=1, padx=5)
                self.processes.append(
                    (arrival_time_entry, burst_time_entry, priority_entry)
                )
            else:
                self.processes.append((arrival_time_entry, burst_time_entry, None))

            # Quantum Field (only displayed if Round Robin is selected)
            if self.scheduler_type_var.get() == "Round Robin":
                quantum_label = ttk.Label(
                    process_frame,
                    text=f"Quantum for Process {i+1}:",
                    font=("Arial", 12),
                )
                quantum_label.grid(row=3, column=0, padx=5, sticky="e")

                quantum_entry = ttk.Entry(process_frame, font=("Arial", 12), width=10)
                quantum_entry.grid(row=3, column=1, padx=5)
                self.processes[-1] += (quantum_entry,)

        # Add "Add Processes" button
        self.add_process_button = ttk.Button(
            self.process_frame, text="Add Processes", command=self.add_processes
        )
        self.add_process_button.pack(pady=10)

        self.go_back_button = ttk.Button(
            self.process_frame,
            text="Go Back",
            command=lambda: self.notebook.select(self.scheduler_frame),
        )
        self.go_back_button.pack()

        # Show the process entry page
        self.notebook.select(self.process_frame)

    def add_processes(self):
        # Collect process details and add them to the list
        process_data = []
        for i, (
            arrival_time_entry,
            burst_time_entry,
            priority_entry,
            *quantum_entry,
        ) in enumerate(self.processes):
            arrival_time = arrival_time_entry.get()
            burst_time = burst_time_entry.get()

            # Validate the inputs
            if not arrival_time or not burst_time:
                messagebox.showerror(
                    "Error",
                    f"Please enter both arrival time and burst time for Process {i+1}.",
                )
                return
            try:
                arrival_time = int(arrival_time)
                burst_time = int(burst_time)
            except ValueError:
                messagebox.showerror(
                    "Error",
                    f"Invalid input: Arrival Time and Burst Time must be integers for Process {i+1}.",
                )
                return

            # Handle priority if applicable
            if priority_entry:
                priority = priority_entry.get()
                if not priority:
                    messagebox.showerror(
                        "Error", f"Please enter priority for Process {i+1}."
                    )
                    return
                try:
                    priority = int(priority)
                except ValueError:
                    messagebox.showerror(
                        "Error",
                        f"Invalid input: Priority must be an integer for Process {i+1}.",
                    )
                    return

            # Handle quantum if applicable (only for Round Robin)
            if self.scheduler_type_var.get() == "Round Robin":
                quantum = quantum_entry[0].get()
                if not quantum:
                    messagebox.showerror(
                        "Error", f"Please enter quantum for Process {i+1}."
                    )
                    return
                try:
                    quantum = int(quantum)
                except ValueError:
                    messagebox.showerror(
                        "Error",
                        f"Invalid input: Quantum must be an integer for Process {i+1}.",
                    )
                    return

            # Store the process data for later use
            process_info = {
                "Process": i + 1,
                "Arrival Time": arrival_time,
                "Burst Time": burst_time,
                "Priority": priority if priority_entry else "N/A",
                "Quantum": quantum if quantum_entry else "N/A",
            }
            process_data.append(process_info)

        # Print the collected process data in the console
        print("\nProcess Data:")
        for data in process_data:
            print(
                f"Process {data['Process']} - Arrival Time: {data['Arrival Time']}, "
                f"Burst Time: {data['Burst Time']}, Priority: {data['Priority']}, Quantum: {data['Quantum']}"
            )

        # Show success message
        messagebox.showinfo("Success", "Processes added successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = CPU_Scheduler_GUI(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox


class CPU_Scheduler_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduler")
        self.root.geometry("600x600")
        self.root.config(bg="#f0f0f0")

        self.processes = []
        self.priority_frame = None
        self.quantum_frame = None

        self.setup_notebook()
        self.create_scheduler_tab()
        self.create_process_tab()
        self.create_gantt_chart_tab()

    def setup_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        self.scheduler_frame = ttk.Frame(self.notebook, padding="10")
        self.process_frame = ttk.Frame(self.notebook, padding="10")
        self.gantt_chart_frame = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.scheduler_frame, text="Scheduler Settings")
        self.notebook.add(self.process_frame, text="Process Entry")
        self.notebook.add(self.gantt_chart_frame, text="Gantt Chart")

    def create_scheduler_tab(self):
        frame = ttk.Frame(self.scheduler_frame)
        frame.pack()

        self.scheduler_type_var = tk.StringVar()

        self.add_labeled_combobox(
            frame, "Select Scheduler Type:", self.scheduler_type_var,
            ["FCFS", "SJF Preemptive", "SJF non_Preemptive",
             "Priority Preemptive", "Priority non_Preemptive", "Round Robin"],
            row=0
        )

        self.num_process_entry = self.add_labeled_entry(
            frame, "Enter Number of Processes:", row=1
        )

        self.next_button = ttk.Button(
            self.scheduler_frame, text="Confirm",
            command=self.show_process_page, width=20
        )
        self.next_button.pack(pady=10)

    def create_process_tab(self):
        self.process_label = ttk.Label(
            self.process_frame, text="Enter Processes Data:", font=("Arial", 14)
        )
        self.process_label.pack(pady=10)

    def create_gantt_chart_tab(self):
        self.process_label = ttk.Label(
            self.gantt_chart_frame, text="Gantt Chart:", font=("Arial", 14)
        )
        self.process_label.pack(pady=10)

    def add_labeled_combobox(self, parent, label_text, var, values, row):
        label = ttk.Label(parent, text=label_text, font=("Arial", 12))
        label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
        combobox = ttk.Combobox(parent, textvariable=var, values=values, state="readonly")
        combobox.grid(row=row, column=1, pady=5)

        return combobox

    def add_labeled_entry(self, parent, label_text, row):
        label = ttk.Label(parent, text=label_text, font=("Arial", 12))
        label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
        entry = ttk.Entry(parent, font=("Arial", 12), width=20)
        entry.grid(row=row, column=1, pady=5, sticky="ew")

        return entry

    def show_process_page(self):
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

        self.reset_process_frame()
        self.generate_process_fields(num_processes)

        ttk.Button(self.process_frame, text="Add Processes", command=self.add_processes).pack(pady=10)
        ttk.Button(self.process_frame, text="Go Back", command=lambda: self.notebook.select(self.scheduler_frame)).pack()
        self.notebook.select(self.process_frame)

    def reset_process_frame(self):
        self.processes = []

        for widget in self.process_frame.winfo_children():
            widget.destroy()

        self.create_process_tab()

    def generate_process_fields(self, count):
        for i in range(count):
            frame = ttk.Frame(self.process_frame)
            frame.pack(pady=5)

            at_entry = self.create_entry_field(frame, f"Arrival Time for Process {i + 1}:", 0)
            bt_entry = self.create_entry_field(frame, f"Burst Time for Process {i + 1}:", 1)

            entries = [at_entry, bt_entry]

            if self.scheduler_type_var.get() in ["Priority Preemptive", "Priority non_Preemptive"]:
                pr_entry = self.create_entry_field(frame, f"Priority for Process {i + 1}:", 2)
                entries.append(pr_entry)
            else:
                entries.append(None)

            if self.scheduler_type_var.get() == "Round Robin":
                qt_entry = self.create_entry_field(frame, f"Quantum for Process {i + 1}:", 3)
                entries.append(qt_entry)

            self.processes.append(tuple(entries))

    def create_entry_field(self, parent, label_text, row):
        label = ttk.Label(parent, text=label_text, font=("Arial", 12))
        label.grid(row=row, column=0, padx=5, sticky="e")
        entry = ttk.Entry(parent, font=("Arial", 12), width=10)
        entry.grid(row=row, column=1, padx=5)

        return entry

    def add_processes(self):
        process_data = []
        for i, fields in enumerate(self.processes):
            arrival, burst, priority, *quantum = fields

            try:
                at = int(arrival.get())
                bt = int(burst.get())
            except ValueError:
                self.show_input_error(i + 1, "Arrival Time and Burst Time must be integers.")
                return

            pr = self.validate_optional_field(priority, i, "Priority") if priority else "N/A"
            if pr is False:
                return

            qt = self.validate_optional_field(quantum[0], i, "Quantum") if quantum else "N/A"
            if qt is False:
                return

            process_data.append({
                "Process": i + 1,
                "Arrival Time": at,
                "Burst Time": bt,
                "Priority": pr,
                "Quantum": qt,
            })

        print("\nProcess Data:")
        for data in process_data:
            print(data)
        messagebox.showinfo("Success", "Processes added successfully!")

    def validate_optional_field(self, field, index, field_name):
        value = field.get()
        if not value:
            messagebox.showerror("Error", f"Please enter {field_name} for Process {index + 1}.")
            return False
        try:
            return int(value)
        except ValueError:
            messagebox.showerror("Error", f"Invalid input: {field_name} must be an integer for Process {index + 1}.")
            return False

    def show_input_error(self, process_num, message):
        messagebox.showerror("Error", f"Process {process_num}: {message}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CPU_Scheduler_GUI(root)
    root.mainloop()

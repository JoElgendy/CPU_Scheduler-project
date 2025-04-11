import tkinter as tk
from tkinter import ttk, messagebox
from utils import generate_color
import random
from schedulers import Process, RoundRobin

class CPU_Scheduler_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduler")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        self.processes = []
        self.tasks = []
        self.priority_frame = None
        self.gantt_canvas = None
        self.gantt_time_unit = 1000

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

        if not scheduler:
            messagebox.showerror("Error", "Please select a scheduler type.")
            return

        is_num_processes_valid, num_processes = self.validate_positive_int_field(self.num_process_entry, "processes count")

        if not is_num_processes_valid:
            return

        self.reset_process_frame()
        self.generate_process_fields(num_processes)

        ttk.Button(self.process_frame, text="Add Processes", command=self.handle_process_submit).pack(pady=10)
        ttk.Button(self.process_frame, text="Go Back", command=lambda: self.notebook.select(self.scheduler_frame)).pack()

        self.notebook.select(self.process_frame)

    def reset_process_frame(self):
        self.processes = []

        for widget in self.process_frame.winfo_children():
            widget.destroy()

        self.create_process_tab()

    def generate_process_fields(self, count):
        if self.scheduler_type_var.get() == "Round Robin":
            frame = ttk.Frame(self.process_frame)

            self.time_quantum_field = self.create_entry_field(frame, f"Time Quantum:", 0)

            frame.pack()

        for i in range(count):
            frame = ttk.Frame(self.process_frame)
            entries = self.populate_process_fields(frame, i + 1)
            frame.pack(pady=10)

            self.processes.append(entries)

    def populate_process_fields(self, frame, pid):
            at_entry = self.create_entry_field(frame, f"Arrival Time for Process {pid}:", 0)
            bt_entry = self.create_entry_field(frame, f"Burst Time for Process {pid}:", 1)
            pr_entry = None

            if self.scheduler_type_var.get() in ["Priority Preemptive", "Priority non_Preemptive"]:
                pr_entry = self.create_entry_field(frame, f"Priority for Process {pid}:", 2)

            return at_entry, bt_entry, pr_entry

    def create_entry_field(self, parent, label_text, row):
        label = ttk.Label(parent, text=label_text, font=("Arial", 12))
        label.grid(row=row, column=0, padx=5, sticky="e")
        entry = ttk.Entry(parent, font=("Arial", 12), width=10)
        entry.grid(row=row, column=1, padx=5)

        return entry

    def handle_process_submit(self):
        self.gantt_to_be_rendered_task_idx = -1
        self.tasks = []
        self.tq = None

        # todo
        is_live = True

        process_data = self.capture_processes_data()

        scheduler = RoundRobin.RoundRobin(self.tq)

        for process in process_data:
            scheduler.addProcess(process)

        self.notebook.select(self.gantt_chart_frame)

        if is_live:
            self.run_live_gantt_chart(scheduler)
        else:
            self.run_fast_gantt_chart(scheduler)

    def capture_processes_data(self):
        process_data = []
        is_round_robin = self.scheduler_type_var.get() == "Round Robin"

        if is_round_robin:
            is_tq_valid, self.tq = self.validate_positive_int_field(self.time_quantum_field, f"time quantum")

        for i, fields in enumerate(self.processes):
            arrival, burst, priority = fields
            pid = i + 1

            is_at_valid, at = self.validate_positive_int_field(arrival, f"arrival time for process {pid}")
            is_bt_valid, bt = self.validate_positive_int_field(burst, f"burst time for process {pid}")
            is_pr_valid, pr = self.validate_positive_int_field(priority, f"priority for process {pid}") if priority else (False, -1)

            if not is_bt_valid or not is_at_valid or (priority and not is_pr_valid) or (is_round_robin and not is_tq_valid):
                return

            process_data.append(Process.Process(pid, at, bt, pr))

        return process_data

    def run_live_gantt_chart(self, scheduler):
        if not scheduler.allProcessesCompleted():
            scheduler.scheduleStep()

        self.tasks = scheduler.occupying

        self.gantt_to_be_rendered_task_idx += 1

        if self.gantt_canvas:
            self.gantt_canvas.delete('all')

        self.draw_gantt_chart()
        
        if len(self.tasks) > self.gantt_to_be_rendered_task_idx:
            self.gantt_chart_frame.after(self.gantt_time_unit + 200, lambda: self.run_live_gantt_chart(scheduler))


    def run_fast_gantt_chart(self, scheduler):
        while not schduler.allProcessesCompleted():
            scheduler.scheduleStep()

        self.tasks = scheduler.occupying

        self.gantt_to_be_rendered_task_idx = -1

        self.draw_gantt_chart()

    def draw_gantt_chart(self):
        # === Configuration ===
        canvas_height = 200
        canvas_width = 600
        y_offset = 70
        x_offset = 10
        max_visible_time_units = 10

        self.current_index = 0

        total_tasks = len(self.tasks)

        # === Dynamic Sizing ===
        if total_tasks > max_visible_time_units:
            unit_width = (canvas_width - 2 * x_offset) / total_tasks  # Zoom out if too many blocks
        else:
            unit_width = 50

        # === Create Canvas ===
        if not self.gantt_canvas:
            self.gantt_canvas = tk.Canvas(
                self.gantt_chart_frame,
                width=canvas_width,
                height=canvas_height,
                bg="white"
            )

            self.gantt_canvas.pack()

        # === Start Animation ===
        self.animate_task_block(x_offset, y_offset, unit_width, self.gantt_to_be_rendered_task_idx == self.current_index)

    def animate_task_block(self, x_offset, y_offset, unit_width, enable_animation=True):
        frame_delay_ms = 5 if enable_animation else 1            # Delay between animation frames
        animation_duration_ms = self.gantt_time_unit if enable_animation else 1   # Total time for each block animation
        time_text_font = ("Helvetica", 8)
        process_text_font = ("Helvetica", 10)
        bar_height = 30

        if self.current_index >= len(self.tasks):
            return

        # === Current Task Details ===
        task_num = self.tasks[self.current_index]
        task_name = "P" + str(task_num)
        color = generate_color(task_num)

        x_start = x_offset + unit_width * self.current_index
        y_bottom = y_offset + bar_height

        rect = self.gantt_canvas.create_rectangle(x_start, y_offset, x_start, y_bottom, fill=color)
        temp_text = self.gantt_canvas.create_text(x_start, y_offset + 15, anchor="w", text=task_name)

        steps = int(animation_duration_ms / frame_delay_ms)
        pixels_per_step = unit_width / steps

        def expand(step=0):
            if step >= steps:
                self.gantt_canvas.coords(rect, x_start, y_offset, x_start + unit_width, y_bottom)

                # Replace temp text with centered one
                self.gantt_canvas.delete(temp_text)
                self.create_centered_canvas_text(task_name, self.gantt_canvas,
                                                x_start + unit_width / 2, y_offset + 15,
                                                font=process_text_font)

                # Draw time marker below
                self.create_centered_canvas_text(self.current_index + 1, self.gantt_canvas,
                                                x_start + unit_width, y_bottom + 10,
                                                font=time_text_font, fill="gray")

                self.current_index += 1
                self.gantt_canvas.after(
                    1,
                    self.animate_task_block(
                        x_offset,
                        y_offset,
                        unit_width,
                        self.gantt_to_be_rendered_task_idx == self.current_index
                    )
                )
            else:
                current_width = step * pixels_per_step
                self.gantt_canvas.coords(rect, x_start, y_offset, x_start + current_width, y_bottom)
                self.gantt_canvas.coords(temp_text, x_start + current_width / 2, y_offset + 15)
                self.gantt_canvas.after(frame_delay_ms, lambda: expand(step + 1))

        expand()

    def create_centered_canvas_text(self, text, canvas, x, y, font=("Helvetica", 10), fill="black"):
        text_id = canvas.create_text(x, y, anchor="w", text=text, font=font, fill=fill)
        bbox = canvas.bbox(text_id)
        text_width = bbox[2] - bbox[0]
        canvas.coords(text_id, x - text_width / 2, y)

    def validate_positive_int_field(self, field, field_name):
        value = field.get()

        if not value:
            messagebox.showerror("Error", f"Please enter {field_name}")
            return False, -1
        try:
            if int(value) >= 0:
                return True, int(value)
            else:
                messagebox.showerror("Error", f"Invalid input: {field_name} must be a positive integer")
                return False, -1

        except ValueError:
            messagebox.showerror("Error", f"Invalid input: {field_name} must be an integer")
            return False, -1

if __name__ == "__main__":
    root = tk.Tk()
    app = CPU_Scheduler_GUI(root)
    root.mainloop()

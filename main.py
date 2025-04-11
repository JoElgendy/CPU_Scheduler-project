import tkinter as tk
from gui import CPU_Scheduler_GUI

if __name__ == "__main__":
    root = tk.Tk()
    app = CPU_Scheduler_GUI(root)
    root.mainloop()

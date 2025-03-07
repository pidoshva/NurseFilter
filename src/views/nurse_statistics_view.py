import tkinter as tk

class NursesStatisticalView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root


    def display(self, assigned):
        counts = assigned['Assigned_Nurse'].value_counts()
        stats = tk.Frame(self.root, width=400, height=400)

        most_assigned = counts.idxmax()
        least_assigned = counts.idxmin()
        tk.Label(stats, text=f"Most Assigned Nurse: {most_assigned} ({counts.max()})", font=("Arial",12)).pack(pady=5)
        tk.Label(stats, text=f"Least Assigned Nurse: {least_assigned} ({counts.min()})", font=("Arial",12)).pack(pady=5)

        tk.Label(stats, text="Assignments by Nurse:", font=("Arial",12,"bold")).pack(pady=5)
        for nurse, count in counts.items():
            tk.Label(stats, text=f"{nurse}: {count} assignment(s)", fg="blue").pack(anchor='w', padx=10)
        
        tk.Button(stats, text="Close", command=self.controller.close_nurse_stats).pack(pady=(5,5))

        stats.pack()
        return stats
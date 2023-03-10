import tkinter as tk

from tkinter import ttk
class ExerciseView:

    def __init__(self):
        self.controller = None
        self.root = tk.Tk()
        self.root.title("Exercise Manager")
        self.root.geometry("800x600")
        self.root.configure(bg="white")

        self.title_label = ttk.Label(self.root, text="Exercise Manager")
        self.title_label.pack(side=tk.TOP, pady=40)

        self.info_frame = ttk.Frame(self.root, padding=20)
        self.info_frame.pack(side=tk.TOP, pady=20)

        self.status_frame = ttk.Frame(self.info_frame, padding=20)
        self.status_frame.pack(side=tk.LEFT, pady=20)

        self.time_frame = ttk.Frame(self.info_frame, padding=20)
        self.time_frame.pack(side=tk.LEFT, pady=20)
        
        self.status_label = ttk.Label(self.status_frame, text="Exercise status: ")
        self.status_label.pack(side=tk.LEFT, padx=20)

        self.time_label = ttk.Label(self.time_frame, text="Exercise time: ")
        self.time_label.pack(side=tk.LEFT)

    def set_controller(self, controller):
        self.controller = controller

        self.btn_frame = ttk.Frame(self.root, padding=20)
        self.btn_frame.pack(side=tk.TOP, pady=20)

        self.exercise_status_label = ttk.Label(self.status_frame, text=self.controller.get_exercise_status(), width=15)
        self.exercise_status_label.pack(side=tk.LEFT)

        self.exercise_time_label = ttk.Label(self.time_frame, text=self.controller.get_exercise_time(), width=15)
        self.exercise_time_label.pack(side=tk.LEFT)

        self.start_btn = ttk.Button(self.btn_frame, text="Start exercise", command=self.on_start_exercise_btn)
        self.start_btn.configure(state='normal')
        self.start_btn.pack(side=tk.LEFT, padx=10)

        self.resume_btn = ttk.Button(self.btn_frame, text="Resume exercise", command=self.on_resume_exercise_btn)
        self.resume_btn.configure(state='disabled')
        self.resume_btn.pack(side=tk.LEFT, padx=10)

        self.pause_btn = ttk.Button(self.btn_frame, text="Pause exercise", command=self.on_pause_exercise_btn)
        self.pause_btn.configure(state='disabled')
        self.pause_btn.pack(side=tk.LEFT, padx=10)

        self.stop_btn = ttk.Button(self.btn_frame, text="Stop exercise", command=self.on_stop_exercise_btn)
        self.stop_btn.configure(state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=10)
    
    def update_data(self):
        self.exercise_status_label.config(text=self.controller.get_exercise_status(), width=15)
        self.exercise_time_label.config(text=self.controller.get_exercise_time(), width=15)
        self.root.after(100, self.update_data)
    
    def on_start_exercise_btn(self):
        self.controller.start_exercise()
        self.exercise_status_label.config(text=self.controller.get_exercise_status(), width=15)
        self.start_btn.configure(state='disabled')
        self.resume_btn.configure(state='disabled')
        self.pause_btn.configure(state='normal')
        self.stop_btn.configure(state='normal')
    
    def on_resume_exercise_btn(self):
        self.controller.start_exercise()
        self.exercise_status_label.config(text=self.controller.get_exercise_status(), width=15)
        self.start_btn.configure(state='disabled')
        self.resume_btn.configure(state='disabled')
        self.pause_btn.configure(state='normal')
        self.stop_btn.configure(state='normal')
    
    def on_pause_exercise_btn(self):
        self.controller.pause_exercise()
        self.exercise_status_label.config(text=self.controller.get_exercise_status(), width=15)
        self.start_btn.configure(state='disabled')
        self.resume_btn.configure(state='normal')
        self.pause_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
    
    def on_stop_exercise_btn(self):
        self.controller.stop_exercise()
        self.exercise_status_label.config(text=self.controller.get_exercise_status(), width=15)
        self.start_btn.configure(state='normal')
        self.resume_btn.configure(state='disabled')
        self.pause_btn.configure(state='disabled')
        self.stop_btn.configure(state='disabled')
    
    def run(self):
        self.update_data()
        self.root.mainloop()
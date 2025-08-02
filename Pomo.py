import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import json
import os
from datetime import datetime

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("500x400")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)
        
        # Timer variables
        self.time_left = tk.IntVar()
        self.timer_running = False
        self.timer_thread = None
        self.current_mode = "work"  # work, short_break, long_break
        
        # Default times (in minutes)
        self.work_time = 25
        self.short_break_time = 5
        self.long_break_time = 15
        self.pomodoros_before_long_break = 4
        
        # Session tracking
        self.completed_pomodoros = 0
        self.total_work_time = 0
        
        # Load settings if they exist
        self.load_settings()
        
        self.setup_ui()
        self.reset_timer()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="🍅 Pomodoro Timer", 
                              font=("Arial", 24, "bold"), 
                              bg="#2c3e50", fg="white")
        title_label.pack(pady=(0, 20))
        
        # Timer display frame
        timer_frame = tk.Frame(main_frame, bg="#34495e", relief="raised", bd=2)
        timer_frame.pack(pady=20, padx=20, fill="x")
        
        # Mode label
        self.mode_label = tk.Label(timer_frame, text="Work Time", 
                                  font=("Arial", 16, "bold"), 
                                  bg="#34495e", fg="white")
        self.mode_label.pack(pady=(10, 5))
        
        # Time display
        self.time_display = tk.Label(timer_frame, text="25:00", 
                                    font=("Arial", 48, "bold"), 
                                    bg="#34495e", fg="#e74c3c")
        self.time_display.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(timer_frame, length=300, mode='determinate')
        self.progress.pack(pady=(0, 10))
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg="#2c3e50")
        control_frame.pack(pady=20)
        
        # Control buttons
        self.start_button = tk.Button(control_frame, text="Start", 
                                     command=self.start_timer,
                                     font=("Arial", 12, "bold"),
                                     bg="#27ae60", fg="white",
                                     width=10, height=2)
        self.start_button.pack(side="left", padx=5)
        
        self.pause_button = tk.Button(control_frame, text="Pause", 
                                     command=self.pause_timer,
                                     font=("Arial", 12, "bold"),
                                     bg="#f39c12", fg="white",
                                     width=10, height=2,
                                     state="disabled")
        self.pause_button.pack(side="left", padx=5)
        
        self.reset_button = tk.Button(control_frame, text="Reset", 
                                     command=self.reset_timer,
                                     font=("Arial", 12, "bold"),
                                     bg="#e74c3c", fg="white",
                                     width=10, height=2)
        self.reset_button.pack(side="left", padx=5)
        
        # Mode selection frame
        mode_frame = tk.Frame(main_frame, bg="#2c3e50")
        mode_frame.pack(pady=20)
        
        # Mode buttons
        work_btn = tk.Button(mode_frame, text="Work", 
                            command=lambda: self.set_mode("work"),
                            font=("Arial", 10, "bold"),
                            bg="#e74c3c", fg="white",
                            width=8)
        work_btn.pack(side="left", padx=5)
        
        short_break_btn = tk.Button(mode_frame, text="Short Break", 
                                   command=lambda: self.set_mode("short_break"),
                                   font=("Arial", 10, "bold"),
                                   bg="#3498db", fg="white",
                                   width=8)
        short_break_btn.pack(side="left", padx=5)
        
        long_break_btn = tk.Button(mode_frame, text="Long Break", 
                                  command=lambda: self.set_mode("long_break"),
                                  font=("Arial", 10, "bold"),
                                  bg="#9b59b6", fg="white",
                                  width=8)
        long_break_btn.pack(side="left", padx=5)
        
        # Stats frame
        stats_frame = tk.Frame(main_frame, bg="#34495e", relief="raised", bd=2)
        stats_frame.pack(pady=20, padx=20, fill="x")
        
        # Stats labels
        stats_title = tk.Label(stats_frame, text="Session Statistics", 
                              font=("Arial", 14, "bold"), 
                              bg="#34495e", fg="white")
        stats_title.pack(pady=(10, 5))
        
        self.stats_label = tk.Label(stats_frame, 
                                   text="Completed Pomodoros: 0 | Total Work Time: 0 min", 
                                   font=("Arial", 10), 
                                   bg="#34495e", fg="white")
        self.stats_label.pack(pady=(0, 10))
        
        # Settings button
        settings_btn = tk.Button(main_frame, text="⚙️ Settings", 
                                command=self.open_settings,
                                font=("Arial", 10),
                                bg="#95a5a6", fg="white")
        settings_btn.pack(pady=10)
        
    def set_mode(self, mode):
        self.current_mode = mode
        self.timer_running = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()
        
        if mode == "work":
            self.time_left.set(self.work_time * 60)
            self.mode_label.config(text="Work Time", fg="#e74c3c")
        elif mode == "short_break":
            self.time_left.set(self.short_break_time * 60)
            self.mode_label.config(text="Short Break", fg="#3498db")
        elif mode == "long_break":
            self.time_left.set(self.long_break_time * 60)
            self.mode_label.config(text="Long Break", fg="#9b59b6")
        
        self.update_display()
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        
    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_button.config(state="disabled")
            self.pause_button.config(state="normal")
            self.timer_thread = threading.Thread(target=self.timer_loop)
            self.timer_thread.daemon = True
            self.timer_thread.start()
    
    def pause_timer(self):
        self.timer_running = False
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
    
    def reset_timer(self):
        self.timer_running = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()
        
        self.set_mode(self.current_mode)
    
    def timer_loop(self):
        while self.timer_running and self.time_left.get() > 0:
            time.sleep(1)
            if self.timer_running:
                self.time_left.set(self.time_left.get() - 1)
                self.root.after(0, self.update_display)
        
        if self.time_left.get() <= 0:
            self.root.after(0, self.timer_finished)
    
    def update_display(self):
        minutes = self.time_left.get() // 60
        seconds = self.time_left.get() % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.time_display.config(text=time_str)
        
        # Update progress bar
        if self.current_mode == "work":
            total_time = self.work_time * 60
        elif self.current_mode == "short_break":
            total_time = self.short_break_time * 60
        else:
            total_time = self.long_break_time * 60
        
        progress_value = ((total_time - self.time_left.get()) / total_time) * 100
        self.progress['value'] = progress_value
    
    def timer_finished(self):
        self.timer_running = False
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        
        # Play notification sound (system beep)
        self.root.bell()
        
        # Show notification
        if self.current_mode == "work":
            self.completed_pomodoros += 1
            self.total_work_time += self.work_time
            self.update_stats()
            
            if self.completed_pomodoros % self.pomodoros_before_long_break == 0:
                messagebox.showinfo("Pomodoro Complete!", 
                                  f"Great job! You've completed {self.completed_pomodoros} pomodoros.\n"
                                  f"Time for a long break!")
                self.set_mode("long_break")
            else:
                messagebox.showinfo("Pomodoro Complete!", 
                                  f"Work session complete! Take a short break.")
                self.set_mode("short_break")
        else:
            messagebox.showinfo("Break Complete!", 
                              "Break time is over! Ready to work?")
            self.set_mode("work")
    
    def update_stats(self):
        self.stats_label.config(text=f"Completed Pomodoros: {self.completed_pomodoros} | "
                                   f"Total Work Time: {self.total_work_time} min")
    
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x250")
        settings_window.configure(bg="#2c3e50")
        settings_window.resizable(False, False)
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings frame
        settings_frame = tk.Frame(settings_window, bg="#2c3e50")
        settings_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title = tk.Label(settings_frame, text="Timer Settings", 
                        font=("Arial", 16, "bold"), 
                        bg="#2c3e50", fg="white")
        title.pack(pady=(0, 20))
        
        # Work time
        tk.Label(settings_frame, text="Work Time (minutes):", 
                bg="#2c3e50", fg="white").pack()
        work_time_var = tk.StringVar(value=str(self.work_time))
        work_time_entry = tk.Entry(settings_frame, textvariable=work_time_var, width=10)
        work_time_entry.pack(pady=(0, 10))
        
        # Short break time
        tk.Label(settings_frame, text="Short Break (minutes):", 
                bg="#2c3e50", fg="white").pack()
        short_break_var = tk.StringVar(value=str(self.short_break_time))
        short_break_entry = tk.Entry(settings_frame, textvariable=short_break_var, width=10)
        short_break_entry.pack(pady=(0, 10))
        
        # Long break time
        tk.Label(settings_frame, text="Long Break (minutes):", 
                bg="#2c3e50", fg="white").pack()
        long_break_var = tk.StringVar(value=str(self.long_break_time))
        long_break_entry = tk.Entry(settings_frame, textvariable=long_break_var, width=10)
        long_break_entry.pack(pady=(0, 10))
        
        # Pomodoros before long break
        tk.Label(settings_frame, text="Pomodoros before long break:", 
                bg="#2c3e50", fg="white").pack()
        pomodoros_var = tk.StringVar(value=str(self.pomodoros_before_long_break))
        pomodoros_entry = tk.Entry(settings_frame, textvariable=pomodoros_var, width=10)
        pomodoros_entry.pack(pady=(0, 20))
        
        # Save button
        def save_settings():
            try:
                self.work_time = int(work_time_var.get())
                self.short_break_time = int(short_break_var.get())
                self.long_break_time = int(long_break_var.get())
                self.pomodoros_before_long_break = int(pomodoros_var.get())
                self.save_settings()
                self.reset_timer()
                settings_window.destroy()
                messagebox.showinfo("Success", "Settings saved successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers!")
        
        save_btn = tk.Button(settings_frame, text="Save Settings", 
                            command=save_settings,
                            bg="#27ae60", fg="white",
                            font=("Arial", 10, "bold"))
        save_btn.pack()
    
    def save_settings(self):
        settings = {
            "work_time": self.work_time,
            "short_break_time": self.short_break_time,
            "long_break_time": self.long_break_time,
            "pomodoros_before_long_break": self.pomodoros_before_long_break
        }
        
        try:
            with open("pomodoro_settings.json", "w") as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def load_settings(self):
        try:
            if os.path.exists("pomodoro_settings.json"):
                with open("pomodoro_settings.json", "r") as f:
                    settings = json.load(f)
                    self.work_time = settings.get("work_time", 25)
                    self.short_break_time = settings.get("short_break_time", 5)
                    self.long_break_time = settings.get("long_break_time", 15)
                    self.pomodoros_before_long_break = settings.get("pomodoros_before_long_break", 4)
        except Exception as e:
            print(f"Error loading settings: {e}")

def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()


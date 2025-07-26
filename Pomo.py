# This is a basic pomodoro timer application in Python.

# Import necessary libraries
import datetime as dt, math, json, tkinter as tk

# Intitialise the window
window = tk.Tk()
window.title("Pomodoro Timer")
window.geometry("400x300")
window.configure(bg="black")
window.mainloop()

# Create a canvas for the timer
canvas = tk.Canvas(window, width=400, height=300, bg="red", highlightthickness=0, border=2)
canvas.place(anchor=tk.CENTER)

timerCircle = canvas.create_oval(50, 50, 350, 250, fill="white")
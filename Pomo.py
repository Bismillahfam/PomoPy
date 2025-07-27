# This is a basic pomodoro timer application in Python.

# Import necessary libraries
import datetime as dt, math, json, tkinter as tk

# Intitialise the window
window = tk.Tk()
window.title("Pomodoro Timer")
window.geometry("400x300")
window.configure(bg="black")


# Canvas for the timer
canvas = tk.Canvas(window, width=400, height=300, bg="white", highlightthickness=0)
canvas.anchor = "center"
canvas.pack()

window.mainloop()
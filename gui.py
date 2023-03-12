"""Will create a GUI to be integrated with the rest of the code."""

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk


def gcode_pressed():
    """Change the text on the screen to say G-code Mode."""
    lbl_value.config(text="G-code Mode \nEnter file name below:")
    inputfile.grid(row=1, column=1, sticky="nsew")
    btn_run_file.grid(row=2, column=1, sticky=NSEW)
    return


def analog_pressed():
    """Change the text on the screen to say G-code Mode."""
    lbl_value.config(text="Analog Mode")
    inputfile.grid_forget()
    btn_run_file.grid_forget()
    return


def run_gcode():
    """Fill in the rest of the code with your functions to run the gcode."""
    file_name = inputfile.get(1.0, END)
    print(file_name)
    return


window = tk.Tk()
window.title("Robotic Arm Interface")
lbl_value = tk.Label(master=window, text="Select a mode")
lbl_value.grid(row=0, column=1)
window.rowconfigure([0, 1, 2], minsize=200, weight=1)
window.columnconfigure([0, 1, 2], minsize=200, weight=1)
btn_gcode_mode = tk.Button(master=window, text="G-code Mode",
                           command=gcode_pressed,)
btn_gcode_mode.grid(row=0, column=0, sticky="nsew")

btn_analog_mode = tk.Button(master=window, text="Analog Mode",
                            command=analog_pressed)
btn_analog_mode.grid(row=0, column=2, sticky="nsew")

inputfile = tk.Text(window, height=10, width=10)

btn_run_file = tk.Button(window, text="Click here to run file",
                         command=run_gcode)


window.mainloop()

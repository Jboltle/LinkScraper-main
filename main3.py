import tkinter as tk
from tkinter import messagebox
print(tk.TkVersion)


root = tk.Tk()
root.withdraw()  # Hide the main window

messagebox.showinfo("Information", "This is an information message.")

root.destroy()  # Close the main window
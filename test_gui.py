import tkinter as tk

root = tk.Tk()
root.title("TEST WINDOW")
root.geometry("300x200")

tk.Label(root, text="Tkinter is working").pack(pady=50)

root.mainloop()

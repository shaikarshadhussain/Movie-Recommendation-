import tkinter as tk

from database import create_database, seed_demo_data
from movie_screen import show_movies
from theme import style_root


create_database()
seed_demo_data()

root = tk.Tk()
root.title("MoodStream | Movie Recommendation")
root.geometry("1366x860")
root.minsize(1100, 720)
style_root(root)

show_movies(root)

root.mainloop()

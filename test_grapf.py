import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_plot_in_tkinter():
    root = tk.Tk()
    root.title("Тестовий графік Matplotlib у Tkinter")

    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot([1, 2, 3, 4], [10, 40, 20, 50])
    ax.set_title("Простий графік")
    ax.set_xlabel("X-вісь")
    ax.set_ylabel("Y-вісь")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    create_plot_in_tkinter()
import functools
import pkg_resources
import queue
import threading
import tkinter as tk


# Variables
destroyed = False
root = None

# Constants
interval = 100
tasks = queue.Queue()
ui_thread = threading.current_thread()


def run_ui(task, *args, **kwargs):
    tasks.put((task, args, kwargs))


def ui_method(f):
    @functools.wraps(f)
    def d(*args, **kwargs):
        if threading.current_thread() == ui_thread:
            return f(*args, **kwargs)
        else:
            run_ui(f, *args, **kwargs)
            return None
    return d


class Application(tk.Canvas):

    def __init__(self, master):
        super(Application, self).__init__(master,
                                          bg='black',
                                          highlightthickness=0,
                                          width=800,
                                          height=500)
        self.ref = []           # Holds references to prevent GC
        self.pbar = None        # Progress bar ID
        self.text = None        # Text widget ID

        self.create_ui()

        # Initial state
        self.set_text('')
        self.set_progress(0)

        self.pack()

    def create_ui(self):
        # Progress bar
        pbar_file = pkg_resources.resource_filename(
            'zen_launcher_resources', 'images/progress_bar.png'
        )
        pbar_image = tk.PhotoImage(file=pbar_file)
        self.ref.append(pbar_image)
        self.pbar = self.create_image((400, 300), image=pbar_image)

        # Image
        background_file = pkg_resources.resource_filename(
            'zen_launcher_resources', 'images/background.png'
        )
        background_image = tk.PhotoImage(file=background_file)
        self.ref.append(background_image)
        self.create_image((400, 250), image=background_image)

        # Text
        self.text = self.create_text(
            (400, 270),
            # fill='#00b5ff',
            justify=tk.CENTER,
            text='',
            font=(None, 9, 'bold')
        )

    @ui_method
    def set_text(self, s, color='#00b5ff'):
        self.itemconfig(self.text, fill=color, text=s.upper())

    @ui_method
    def set_progress(self, p):
        if not isinstance(p, int):
            p = int(p)
        if p < 0 or 100 < p:
            raise ValueError
        x, y = 4 * p, 300
        self.coords(self.pbar, (x, y))


def destroy():
    global destroyed
    destroyed = True

    # Wait INTERVAL so
    root.after(interval, root.destroy)


def create_window():
    global root
    root = tk.Tk()
    # root.overrideredirect(1)
    root.protocol('WM_DELETE_WINDOW', destroy)

    def process():
        if destroyed:
            return

        while 1:
            try:
                f, args, kwargs = tasks.get_nowait()
            except queue.Empty:
                break
            else:
                f(*args, **kwargs)

        # Enqueue again
        root.after(interval, process)

    # Enqueue initially
    root.after(interval, process)

    root.wm_resizable(0, 0)
    return Application(master=root)


def run():
    tk.mainloop()

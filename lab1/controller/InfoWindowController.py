import tkinter
from view.InfoView import InfoView


class InfoWindowController:
    def __init__(self):
        self.window = None

    def open_window(self):
        if self.window is not None:
            try:
                if self.window.winfo_exists():
                    self.window.destroy()
            except tkinter.TclError:
                pass
        self.window = InfoView(self)
        self.window.main()


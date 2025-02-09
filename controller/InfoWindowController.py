from view.InfoView import InfoView
from logger import logger

class InfoWindowController:
    def __init__(self):
        self.window = None

    def open_window(self):
        if self.window is not None and self.window.winfo_exists():
            self.window.destroy()
        self.window = InfoView(self)
        self.window.main()


from importlib import import_module

from view.StartView import StartView
from controller.MainWindowController import  MainWindowController
from controller.InfoWindowController import  InfoWindowController


class UltimateController:
    def __init__(self):
        self.start_view = StartView(self)
        self.info_window_controller = InfoWindowController()
        self.main_window_controller = MainWindowController()
        self.file = None

    def open_start_view(self):
        self.start_view.main()

    def open_info_view(self):
        self.info_window_controller.open_window()

    def open_main_view(self):
        self.main_window_controller.open_window()


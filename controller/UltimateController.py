from importlib import import_module

from view.StartView import StartView
from view.InfoView import InfoView
from controller.MainWindowController import  MainWindowController
# пока главный контроллер отвечает за все, предлагаю потом разбить
# на более мелкие

class UltimateController:
    def __init__(self):
        self.start_view = StartView(self)
        self.info_view = None  # Изменено на None, чтобы инициализировать позже
        self.main_window_controller = MainWindowController()  # Изменено на None, чтобы инициализировать позже
        self.file = None

    def open_start_view(self):
        self.start_view.main()

    def open_info_view(self):
        if self.info_view is None:  # Инициализация только при необходимости
            self.info_view = InfoView(self)
        self.info_view.main()

    def open_main_view(self):
        self.main_window_controller.open_window()

    def open_file(self, file):
        self.main_window_controller.open_file(file)

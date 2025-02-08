from scr.StartView import StartView
from scr.InfoView import InfoView
from scr.MainView import MainView

# пока главный контроллер отвечает за все, предлагаю потом разбить
# на более мелкие

class UltimateController:
    def __init__(self):
        self.start_view = StartView(self)
        self.info_view = None  # Изменено на None, чтобы инициализировать позже
        self.main_view = None  # Изменено на None, чтобы инициализировать позже
        self.file = None

    def open_start_view(self):
        self.start_view.main()

    def open_info_view(self):
        if self.info_view is None:  # Инициализация только при необходимости
            self.info_view = InfoView(self)
        self.info_view.main()

    def open_main_view(self):
        if self.info_view is not None and self.info_view.winfo_exists():
            # Закрываем второе окно, если оно уже открыто
            self.info_view.destroy()  # Инициализация только при необходимости
        self.main_view = MainView(self)
        self.main_view.main()

    def open_file(self, file):
        # вызов обработчика файлов из model
        # открытие окна текста (я его еще не создала хехе)
        pass


if __name__ == "__main__":
    app = UltimateController()
    app.open_start_view()
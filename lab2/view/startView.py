import tkinter as tk
from tkinter import ttk
from infoView import InfoView
from mainView import CorpusManagerView


class StartView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.configure(bg='lavender blush')
        self.title("Корпусный менеджер")
        self.geometry("800x600")
        self.style = ttk.Style()
        self.style.configure("TButton", background='lavender blush', font=("Helvetica", 13),
                             padding=20)

    def create_widgets(self):
        label = tk.Label(self, text="Добро пожаловать в систему управления корпусом текстов",
                         font=("Helvetica", 14), bg='lavender blush')
        label.place(relx=0.5, rely=0.3, anchor='center')

        start_button = ttk.Button(self, text="Начать работу!", style='TButton', command=lambda: self.open_main_view(),
                                  width=30)
        start_button.place(relx=0.5, rely=0.5, anchor='center')

        about_button = ttk.Button(self, text="О приложении", style='TButton', command=lambda: self.open_info_view(),
                                  width=30)
        about_button.place(relx=0.5, rely=0.7, anchor='center')

    def open_info_view(self):
        InfoView(self)

    def open_main_view(self):
       CorpusManagerView(self)

    def main(self):
        self.create_widgets()
        self.mainloop()

if __name__ == "__main__":
    start_view = StartView()
    start_view.main()
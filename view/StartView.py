import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox, filedialog


class StartView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.configure(bg='lavender blush')
        self.title("Формирование словаря естественного языка")
        self.geometry("600x400")
        self.style = ttk.Style()
        self.style.configure("TButton", background='lavender blush', font=("Helvetica", 13),
                             padding=20)

    def create_widgets(self):

        label = tk.Label(self, text="Добро пожаловать в систему формирования\n словаря естественного языка!",
                         font=("Helvetica", 14), bg='lavender blush')
        label.place(relx=0.5, rely=0.3, anchor='center')

        start_button = ttk.Button(self, text="Начать работу!", style='TButton',command=lambda: self.open_main_view(),  width=30)
        start_button.place(relx=0.5, rely=0.5, anchor='center')

        about_button = ttk.Button(self, text="О приложении", style='TButton', command=lambda: self.open_info_view(), width=30)
        about_button.place(relx=0.5, rely=0.7, anchor='center')

    def open_info_view(self):
        self.controller.open_info_view()
        
    def open_main_view(self):
        self.controller.open_main_view()

    def main(self):
        self.create_widgets()
        self.mainloop()


# код для проверки
if __name__ == "__main__":
    app = StartView()
    app.main()
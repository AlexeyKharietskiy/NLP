import tkinter as tk


class InfoView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.resizable(False, False)
        self.controller = controller
        self.configure(bg='snow1')
        self.title("О программе")
        self.geometry("400x400")

    def create_widgets(self):
        label = tk.Label(self, text="Данная программа предназначена для\n автоматизированного лексического анализа\n"
                                    "текстов естественного языка (ТЕЯ).\n\n"
                                    " В качестве выходных данных вам предо-\nставляется"
                                    " перечень лексем и словоформ,\n упорядоченных по алфавиту с указанием\n частоты их"
                                    "встречаемости и возможностью\n добавления дополнительной морфологической\n"
                                    " информации о них. \nВсе, что нужно программе - это загрузка\n вашего файла!"
                                    "\n\n Программа предоставляет возможность поиска,\n добавления новой информации,"
                                    "\nсохранение Ваших изменений \nв автоматически получаемом словаре.",
                         font=("Helvetica", 13), bg='snow1')
        label.pack(anchor= tk.NW, pady=20)

    def main(self):
        self.create_widgets()
        self.mainloop()
        
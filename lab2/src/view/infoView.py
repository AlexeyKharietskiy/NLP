import tkinter as tk


class InfoView(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.resizable(False, False)
        self.configure(bg='snow1')
        self.title("О программе")
        self.geometry("500x300")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Корпусный менеджер - это электронный ресурс,\n созданный для просмотра и взаимодействия\n с"
                                    " корпусом текстов.\n Корпусный менеджер реализует все важные\n свойства корпуса текстов "
                                    "и предоставляет удобную\n навигацию по нему. В нем вы найдете частотные\n"
                                    " характеристики словоформ, леммы, морфологические\n характеристики"
                                    " словоформ и их метаданные\n (библиографические, типологические),\n а также "
                                    "конкордансные списки.",
                         font=("Helvetica", 13), bg='snow1')
        label.pack(anchor='center', pady=20)

    def main(self):
        self.create_widgets()
        self.mainloop()

if __name__ == "__main__":
    info_view = InfoView()
    info_view.main()
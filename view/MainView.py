import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox, filedialog


# следующий класс просто вставочка с прошлой лабы для раскрутки
# пока просто не обращай внимания

class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title('Лексический словарь')
        self.vocab_table = None
        self.menu = None

    def create_view(self):
        # table
        columns = ["Wordform", "Lemma", "Occurance Frequency", "Morfological Info"]
        self.vocab_table = ttk.Treeview(self, columns=columns, show="headings")
        self.vocab_table.grid(row=0, column=0, padx=[10, 10], pady=10, columnspan=3)
        self.vocab_table.configure(height=30)
        self.vocab_table.heading("Wordform", text="Словоформа")
        self.vocab_table.heading("Lemma", text="Лемма")
        self.vocab_table.heading("Occurance Frequency", text="Частота появления")
        self.vocab_table.heading("Morfological Info", text="Морфологическая Информация")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.vocab_table.yview)
        scrollbar.grid(row=0, column=2, sticky='nse')

        self.menu = tk.Menu(self, bg='lavender blush', fg='black', activebackground='lavender', activeforeground='black')
        self.menu.add_command(label="Открыть файл", command=self.open_file)
        self.config(menu=self.menu)

    def main(self):
        self.create_view()
        self.mainloop()

    def open_file(self):
        filename = filedialog.askopenfilename(title='Открыть файл', filetypes=(("DOCX", "*.docx"), ("DOC", "*.doc")))
        self.controller.open_file(filename)
        # здесь вызыв контроллера чтобы он открыл окно и туда записал текст с файла
        pass

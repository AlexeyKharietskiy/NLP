import tkinter as tk
from tkinter import ttk, filedialog

# следующий класс просто вставочка с прошлой лабы для раскрутки
# пока просто не обращай внимания
class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.resizable(False, False)
        self.controller = controller
        self.title('Лексический словарь')
        self.vocab_table = None
        self.menu = None
        self.search_entry = None  # Поле для ввода поискового запроса
        self.search_button = None  # Кнопка для запуска поиска
        self.full_data = []  # Храним все данные для восстановления после поиска

    def create_view(self):
        # table
        columns = ["Wordform", "Lemma", "Occurance Frequency", "Morfological Info"]
        self.vocab_table = ttk.Treeview(self, columns=columns, show="headings")
        self.vocab_table.grid(row=1, column=0, padx=[10, 10], pady=10, columnspan=3)
        self.vocab_table.configure(height=30)
        self.vocab_table.heading("Wordform", text="Словоформа")
        self.vocab_table.heading("Lemma", text="Лемма")
        self.vocab_table.heading("Occurance Frequency", text="Частота появления")
        self.vocab_table.heading("Morfological Info", text="Морфологическая Информация")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.vocab_table.yview)
        scrollbar.grid(row=1, column=2, sticky='nse')
        self.vocab_table.configure(yscrollcommand=scrollbar.set)

        self.menu = tk.Menu(self, bg='lavender blush', fg='black', activebackground='lavender', activeforeground='black')
        self.menu.add_command(label="Открыть файл", command=self.open_file)
        self.config(menu=self.menu)

        search_label = tk.Label(self, text="Поиск:")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.search_entry = tk.Entry(self, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.search_button = tk.Button(self, text="Найти", command = self.perform_search)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

    def main(self):
        self.create_view()
        self.mainloop()

    def clear_table(self):
        for item in self.vocab_table.get_children():
            self.vocab_table.delete(item)

    def populate_table(self, data):
        self.clear_table()
        for row in data:
            self.vocab_table.insert("", tk.END, values=row)

    def open_file(self):
        filename = filedialog.askopenfilename(title='Открыть файл', filetypes=(("DOCX", "*.docx"), ("DOC", "*.doc")))
        data = self.controller.open_file(filename)
        self.populate_table(data)

    def perform_search(self):
        searched_word_list = self.controller.search_words(self.search_entry.get())
        self.populate_table(searched_word_list)

import tkinter as tk
from tkinter import ttk, filedialog
from logger import logger

class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.resizable(False, False)
        self.controller = controller
        self.title('Лексический словарь')
        self.vocab_table = None
        self.menu = None
        self.search_entry = None
        self.search_button = None
        self.edit_entry = None
        self.current_item = None

    def create_view(self):
        columns = ["Wordform", "Lemma", "Occurance Frequency", "Morfological Info"]
        self.vocab_table = ttk.Treeview(self, columns=columns, show="headings")
        self.vocab_table.grid(row=1, column=0, padx=10, pady=10, columnspan=3)
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
        self.search_entry.bind('<Return>', lambda event: self.perform_search())
        self.search_button = tk.Button(self, text="Найти", command = self.perform_search)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.vocab_table.bind('<Double-1>', self.start_edit)

    def main(self):
        self.create_view()
        self.mainloop()

    def clear_table(self):
        for item in self.vocab_table.get_children():
            self.vocab_table.delete(item)

    def populate_table(self, data):
        self.clear_table()
        try:
            for row in data:
                self.vocab_table.insert("", tk.END, values=row)
        except TypeError as e:
            logger.error(f'{e}, {data}')

    def open_file(self):
        filename = filedialog.askopenfilename(title='Открыть файл', filetypes=(("DOCX", "*.docx"), ("DOC", "*.doc")))
        data = self.controller.open_file(filename)
        self.populate_table(data)

    def perform_search(self):
        searched_word_list = self.controller.search_words(self.search_entry.get())
        self.populate_table(searched_word_list)

    def start_edit(self, event):
        col = self.vocab_table.identify_column(event.x)
        if col == "#4":
            item = self.vocab_table.identify_row(event.y)
            if item != self.current_item:
                self.finish_edit()

            self.current_item = item
            cell_value = self.vocab_table.set(item, column="#4")

            if not self.edit_entry:
                self.edit_entry = tk.Entry(self.vocab_table, width=20)
                self.edit_entry.bind('<FocusOut>', self.finish_edit)
                self.edit_entry.bind('<Return>', self.finish_edit)

            bbox = self.vocab_table.bbox(item, "#4")
            if bbox:
                self.edit_entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
                self.edit_entry.delete(0, tk.END)
                self.edit_entry.insert(0, cell_value)
                self.edit_entry.select_range(0, tk.END)
                self.edit_entry.focus_set()

    def finish_edit(self, event=None):
        if self.edit_entry and self.current_item:
            new_value = self.edit_entry.get()
            item_id = self.vocab_table.item(self.current_item)
            word_form = item_id['values'][0]
            self.vocab_table.set(self.current_item, column="#4", value=new_value)

            self.controller.update_word_form_morphological_info(word_form, new_value)

        self.current_item = None
        if self.edit_entry:
            self.edit_entry.destroy()
            self.edit_entry = None
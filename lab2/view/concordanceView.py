import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class ConcordanceView(tk.Toplevel):
    def __init__(self, root, word, words_data):
        super().__init__(root)
        self.resizable(False, False)
        self.title("Конкорданс слова")
        self.geometry("1200x600")

        self.word = word
        self.words_data = words_data
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.text = ScrolledText(main_frame, wrap=tk.WORD, font=('Courier', 10))
        self.text.pack(expand=True, fill=tk.BOTH)

        # Настройка подсветки
        self.text.tag_config("highlight", background="LightSeaGreen")

        for row in self.words_data:
            left_context = " ".join(row.get('left_context', ''))
            right_context = " ".join(row.get('right_context', ''))
            start = len(left_context) + 4
            end = start + len(row.get('word', ''))
            line_num = int(self.text.index(tk.END).split('.')[0])-1
            line = '...' + left_context + ' ' + row.get('word', '') + ' ' + right_context + '...\n'+'\n'
            self.text.insert(tk.END, line)
            self.text.tag_add("highlight",
                              f"{line_num}.{start}",
                              f"{line_num}.{end}")





import tkinter as tk
from tkinter import ttk
import requests

from SyntaxTree import SyntaxTreeApp

from logger import logger


class ParsingView(tk.Toplevel):
    def __init__(self, root, sentence_id):
        super().__init__(root)
        self.resizable(False, False)
        self.title("Семантико-синтаксический анализ")
        self.geometry("1200x600")
        self.sentence_id = sentence_id
        self.create_widgets()
        self.fill_in_all_words()
        self.fill_in_all_roles()
        self.bind('<Return>', self.search_by_substr)
        self.bind('<Escape>', self.fill_in_all_words)

    def create_widgets(self):
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_panel = ttk.Frame(main_container, width=int(1200 * 0.7))
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_panel = ttk.Frame(main_container, width=int(1200 * 0.3))
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        controls_frame = tk.Frame(left_panel)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        search_frame = tk.Frame(controls_frame)
        search_frame.pack(side=tk.LEFT)

        self.create_members_combobox(controls_frame)
        self.create_search_entry(search_frame)
        self.create_search_button(search_frame)
        self.create_revert_button(search_frame)
        self.create_tree_button(search_frame)
        self.create_syntax_table(left_panel)
        self.create_semantic_table(right_panel)

    def create_search_entry(self, frame: ttk.Frame):
        tk.Label(frame, text="Поиск:").pack(side=tk.LEFT, padx=(5, 0))
        self.search_entry = ttk.Entry(frame, width=10)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 5))

    def create_members_combobox(self, frame: ttk.Frame):
        tk.Label(frame, text="Часть речи:").pack(side=tk.LEFT, padx=(5, 5))
        poses = ("NOUN", "ADJ", "VERB", "INFN",
                 "PRTF", "PRTS", "NUMR", "ADV",
                 "PRON", "PRED", "ADP", "SCONJ",
                 "CCONJ", "PART", "INTJ", "PROPN", "DET"
        )

        self.members_combobox = ttk.Combobox(
            frame,
            values=poses,
            state="readonly",
            width=10,
            height=50,
        )
        self.members_combobox.pack(side=tk.LEFT, padx=1)
        self.members_combobox.bind("<<ComboboxSelected>>", self.filter_by_criteria)

    def create_revert_button(self, frame: ttk.Frame):
        revert_btn = tk.Button(
            frame,
            text="Сброс",
            command=lambda: [
                self.search_entry.delete(0, tk.END),
                self.fill_in_all_words(),
                self.members_combobox.set("")
            ],
            width=5
        )
        revert_btn.pack(side=tk.LEFT, padx=5)

    def create_tree_button(self, frame: ttk.Frame):
        revert_btn = tk.Button(
            frame,
            text="Показать дерево",
            command=self.show_tree_view,
            width=15
        )
        revert_btn.pack(side=tk.LEFT, padx=10)

    def create_search_button(self, frame: ttk.Frame):
        search_btn = tk.Button(
            frame,
            text="Найти",
            command=lambda: [
                self.search_by_substr(),
                self.members_combobox.set("")
            ],
            width=10
        )
        search_btn.pack(side=tk.LEFT)

    def create_syntax_table(self, frame: ttk.Frame):
        table_frame = tk.Frame(frame, padx=5, pady=5)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("word", "pos", "info")

        self.words_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=25,
            selectmode="browse"
        )

        self.words_table.heading("word", text="Слово")
        self.words_table.heading("pos", text="Часть речи")
        self.words_table.heading("info", text="Морфологическая информация")

        self.words_table.column("word", width=100, anchor=tk.W)
        self.words_table.column("pos", width=100, anchor=tk.W)
        self.words_table.column("info", width=250, anchor=tk.W)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.words_table.yview)
        self.words_table.configure(yscrollcommand=scrollbar.set)

        self.words_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_semantic_table(self, frame: ttk.Frame):
        table_frame = tk.Frame(frame, padx=5, pady=5)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("text", "role")

        self.semantic_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=25,
            selectmode="browse"
        )

        self.semantic_table.heading("text", text="Текст")
        self.semantic_table.heading("role", text="Роль в предложении")

        self.semantic_table.column("text", width=150, anchor=tk.W)
        self.semantic_table.column("role", width=150, anchor=tk.W)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.semantic_table.yview)
        self.semantic_table.configure(yscrollcommand=scrollbar.set)

        self.semantic_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def filter_by_criteria(self, event=None):
        """Fill in words by sentence member

        Args:
            event (_type_, optional): _description_. Defaults to None.
        """
        self.search_entry.delete(0, tk.END)
        criteria = self.members_combobox.get()
        response = requests.get(
            url=f'http://127.0.0.1:8000/words/pos/{self.sentence_id}',
            params={'pos': criteria}
        )
        if response.status_code == 404:
            error_data = response.json()
            logger.error(f"{error_data.get('detail')}")
            self.words_table.delete(*self.words_table.get_children())
        else:
            self.update_words_table(response.json()['data'])

    def search_by_substr(self, event=None):
        """Fill in words by the substr"""
        search_term = self.search_entry.get()
        if not search_term:
            return
        url = f'http://127.0.0.1:8000/words/substr/{self.sentence_id}'
        params = {
            "substr": search_term,
        }
        response = requests.get(url, params=params)
        if response.status_code == 404:
            error_data = response.json()
            logger.error(f"{error_data.get('detail')}")
            self.words_table.delete(*self.words_table.get_children())
        else:
            words = response.json()
            self.update_words_table(words['data'])

    def update_words_table(self, searched_words: list[dict]):
        """Update words in the table

        Args:
            searched_words (list[dict]): words dictionaries
        """
        self.words_table.delete(*self.words_table.get_children())
        if searched_words:
            for word in searched_words:
                values = (
                    word['word'],
                    word['pos'],
                    word['feats'],
                )
                self.words_table.insert("", tk.END, values=values)

    def update_semantic_table(self, searched_roles):
        self.semantic_table.delete(*self.semantic_table.get_children())
        if searched_roles:
            for word in searched_roles:
                values = (
                    word['ner'],
                    word['type'],
                )
                self.semantic_table.insert("", tk.END, values=values)
        else: return

    def fill_in_all_words(self, event=None):
        '''Fill in all the sentence words'''
        response = requests.get(
            f"http://127.0.0.1:8000/morphological_words/{self.sentence_id}"
        )
        if response.status_code == 404:
            error_data = response.json()
            logger.error(f"{error_data.get('detail')}")
            self.words_table.delete(*self.words_table.get_children())
        else:
            words = response.json()['data']
            print(words)
            self.update_words_table(words)

    def fill_in_all_roles(self, event=None):
        '''Fill in all the sentence roles'''
        response = requests.get(
            f"http://127.0.0.1:8000/ners/{self.sentence_id}"
        )
        if response.status_code == 404:
            error_data = response.json()
            logger.error(f"{error_data.get('detail')}")
            self.semantic_table.delete(*self.semantic_table.get_children())
        else:
            roles = response.json()['data']
            self.update_semantic_table(roles)

    def show_tree_view(self):
        app = SyntaxTreeApp(self, self.sentence_id)

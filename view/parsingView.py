import tkinter as tk
from tkinter import ttk
import requests
class ParsingView(tk.Toplevel):
    def __init__(self, root, sentence_id):
        super().__init__(root)
        self.resizable(False, False)
        self.title("Синтаксический анализ предложения")
        self.geometry("1200x600")
        self.sentence_id = sentence_id
        self.create_widgets()
        self.fill_in_all_words()
        self.bind('<Return>', self.search_by_substr)
        self.bind('<Escape>', self.fill_in_all_words)
        
    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(10, 10))
        search_frame = tk.Frame(controls_frame)
        search_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        self.create_members_combobox(controls_frame)
        self.create_search_entry(search_frame)
        self.create_search_button(search_frame)
        self.create_revert_button(search_frame)
        self.create_table(main_frame)
    
    def create_search_entry(self, frame: ttk.Frame):
        tk.Label(frame, text="Поиск:").pack(side=tk.LEFT, padx=(20, 0))
        self.search_entry = ttk.Entry(frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 5))
    
    def create_members_combobox(self, frame: ttk.Frame):
        tk.Label(frame, text="Член предложения:").pack(side=tk.LEFT, padx=(10, 5))
        poses = (
            'сказуемое',
            'подлежащее',
            'прямое дополнение',
            'косвенное дополнение',
            'обстоятельство',
            'обращение',

            'прилагательное-определение',
            'несогласованное определение',
            'пояснение (приложение)',
            'числительное',
            
            'вспомогательный глагол',
            'связка (глагол-связка)',
            'предикативное дополнение',
            'дополнительное предложение',
            'обстоятельственное предложение',
            'придаточное-подлежащее',

            'однородный член',
            'сочинительный союз',

            'определительное предложение',
            'вводная конструкция',
            'устойчивое выражение',
            'составное слово',
            'составное имя',

            'предлог/послелог',
            'подчинительный союз',
            'определитель (артикль/местоимение)',
            'наречие',
            'знак препинания',

            'неясная связь',
            'нестандартная связь',
            'вводное слово',
            'формальное подлежащее'
        )

        self.members_combobox = ttk.Combobox(
            frame,
            values=poses,
            state="readonly",
            width=30
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
            width=8
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
            width=8
        )
        search_btn.pack(side=tk.LEFT)
            
    def create_table(self, frame: ttk.Frame):
        table_frame = tk.Frame(frame, padx=5, pady=5)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("word", "head_word", "part_of_speech")

        self.words_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=17,
            selectmode="browse"
        )

        self.words_table.heading("word", text="Зависимое слово")
        self.words_table.heading("head_word", text="Главное слово")
        self.words_table.heading("part_of_speech", text="Часть речи")

        self.words_table.column("word", width=150, anchor=tk.W)
        self.words_table.column("head_word", width=150, anchor=tk.W)
        self.words_table.column("part_of_speech", width=200, anchor=tk.W)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.words_table.yview)
        self.words_table.configure(yscrollcommand=scrollbar.set)

        self.words_table.pack(side="left", fill="both", expand=True, padx=(5, 2))
        scrollbar.pack(side="right", fill="y", padx=5)
        
    def filter_by_criteria(self, event=None):
        """Fill in words by sentence member

        Args:
            event (_type_, optional): _description_. Defaults to None.
        """
        self.search_entry.delete(0, tk.END)
        criteria = self.members_combobox.get()
        response = requests.get(
            url=f'http://127.0.0.1:8000/words/rel/{self.sentence_id}',
            params={'rel': criteria}
        )
        if response.status_code == 404:
            error_data = response.json()
            print(f"Ошибка: {error_data.get('detail')}")
        else:
            self.update_words_table(response.json()['data'])

    def search_by_substr(self, event):
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
            print(f"Ошибка: {error_data.get('detail')}")
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
                    word['head'],
                    word['relation'],
                )
                self.words_table.insert("", tk.END, values=values)

    def fill_in_all_words(self, event=None):
        '''Fill in all the sentence words'''
        response = requests.get(
            f"http://127.0.0.1:8000/words/{self.sentence_id}"
        )
        words = response.json()['data']
        self.update_words_table(words)


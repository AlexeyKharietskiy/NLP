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
        self.pull_all_words()
    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(10, 10))

        tk.Label(controls_frame, text="Член предложения:").pack(side=tk.LEFT, padx=(10, 5))
        poses = (
            'подлежащее',
            'корневой элемент (сказуемое)',
            'косвенное дополнение',
            'относительное предложение',
            'относительное предложение (специфическое)',
            'обстоятельственное придаточное',
            'обстоятельство',
            'согласованное определение','приложение',
            'вспомогательный глагол',
            'вспомогательный глагол (пассив)',
            'предлог/послелог',
            'сочинительный союз',
            'дополнительное придаточное',
            'классификатор',
            'составная часть',
            'сочинительная связь',
            'связка',
            'предикативное придаточное',
            'предикативное придаточное (пассив)',
            'неопределенная зависимость',
            'определитель',
            'дискурсивный элемент',
            'дислоцированный элемент',
            'эксплетив (формальный субъект)',
            'фиксированное выражение',
            'плоская структура',
            'иностранное слово в составе',
            'имя собственное (составное)',
            'графическое объединение',
            'элемент списка',
            'подчинительный союз',
            'несогласованное определение',
            'внешнее подлежащее',
            'подлежащее (пассив)',
            'числительное как модификатор',
            'числительное-сущность',
            'числительное-главное слово',
            'прямое дополнение',
            'косвенное дополнение',
            'агентивное дополнение',
            'временное обстоятельство',
            'сиротский элемент (в эллипсисе)',
            'паратаксис',
            'элемент для исправления',
            'вокатив',
            'предикативное дополнение',
            'агентивное определение',
            'глагольное подлежащее',
            'глагольное дополнение',
            'притяжательное определение',
        )

        self.part_of_sentence = ttk.Combobox(
            controls_frame,
            values=poses,
            state="readonly",
            width=30
        )
        self.part_of_sentence.pack(side=tk.LEFT, padx=1)
        self.part_of_sentence.current(0)
        self.part_of_sentence.bind("<<ComboboxSelected>>", self.filter_by_criteria)

        search_frame = tk.Frame(controls_frame)
        search_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        tk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT, padx=(20, 0))

        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 5))

        search_btn = tk.Button(
            search_frame,
            text="Найти",
            command=self.search_by_substr,
            width=8
        )
        search_btn.pack(side=tk.LEFT)

        revert_btn = tk.Button(
            search_frame,
            text="Сброс",
            command=lambda: [
                self.search_entry.delete(0, tk.END),
                self.pull_all_words()
            ],
            width=8
        )
        revert_btn.pack(side=tk.LEFT, padx=10)


        table_frame = tk.Frame(main_frame, padx=5,
                               pady=5)
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
        criteria = str(self.part_of_sentence.get())
        response = requests.get(
            f'http://127.0.0.1:8000/words/rel/{self.sentence_id}',
            params={
                'rel': criteria
            }
                                )
        response.raise_for_status()
        self.update_words_table(response.json()['data'])

    def search_by_substr(self):
        search_term = str(self.search_entry.get())
        if not search_term:
            return
        url = f'http://127.0.0.1:8000/words/substr/{self.sentence_id}'
        params = {
            "substr": search_term,
        }
        response_words = requests.get(url, params=params)
        response_words.raise_for_status()
        words = response_words.json()

        self.update_words_table(words['data'])

    def update_words_table(self, searched_words):
        self.words_table.delete(*self.words_table.get_children())
        if searched_words:
            for word in searched_words:
                values = (
                    word['word'],
                    word['head'],
                    word['relation'],
                )
                self.words_table.insert("", tk.END, values=values)

    def pull_all_words(self):
        response = requests.get(
            f"http://127.0.0.1:8000/words/{self.sentence_id}"
        )
        words = response.json()['data']
        self.update_words_table(words)


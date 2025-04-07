import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox, scrolledtext
import os


import requests
from concordanceView import ConcordanceView
from pydantic import BaseModel


class CorpusManagerView(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Корпусный менеджер")
        self.geometry("1200x700")
        self.selected_text = None
        self.concordances = None
        self.style = ttk.Style()
        self.style.configure("TButton", background='grey76', font=("Helvetica", 10),
                             padding=5)

        self.create_menu()

        self.main_panel = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_panel.pack(fill=tk.BOTH, expand=True)

        self.create_texts_table()

        self.right_panel = tk.Frame(self.main_panel, bg="#f0f0f0", padx=10, pady=10)
        self.main_panel.add(self.right_panel)

        self.create_right_panel()

    def create_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Добавить файл", command=self.add_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)

        menubar.add_cascade(label="Файл", menu=file_menu)
        self.config(menu=menubar)

    def create_right_panel(self):
        """Правая панель с информацией о файле"""
        self.right_panel = tk.Frame(self.main_panel, bg="#f0f0f0", padx=5, pady=5)
        self.main_panel.add(self.right_panel)

        # Создаем рамку с рельефом и заголовком
        info_frame = tk.LabelFrame(
            self.right_panel,
            text=" Текст ",
            font=("Arial", 11),
            labelanchor="nw",
            bd=2,
            relief=tk.GROOVE,
            padx=5,
            pady=5
        )
        info_frame.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)

        self.text_info = scrolledtext.ScrolledText(
            info_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            padx=5,
            pady=5,
            bg="white",
            height=10,
        )
        self.text_info.pack(fill=tk.BOTH, expand=False)

        self.text_info.bind("<Button-1>", self.start_editing)

        self.save_button = tk.Button(
            info_frame,
            text="Сохранить",
            command=self.save_text,
            state=tk.DISABLED
        )
        self.save_button.pack(pady=5, anchor='e')

        controls_frame = tk.Frame(self.right_panel)
        controls_frame.pack(fill=tk.X, pady=(30, 0))

        tk.Label(controls_frame, text="Часть речи:").pack(side=tk.LEFT, padx=(0, 5))

        self.part_of_speech = ttk.Combobox(
            controls_frame,
            values=["имя cуществительное", "глагол", "имя прилагательное", "наречие", "местоимение",
                    "предлог", "частица", "междометие", "подчинительный союз", "сочинительный союз",
                    "числительное"],
            state="readonly",
            width=20
        )
        self.part_of_speech.pack(side=tk.LEFT, padx=1)
        self.part_of_speech.current(0)
        self.part_of_speech.bind("<<ComboboxSelected>>", self.filter_by_criteria)

        search_frame = tk.Frame(controls_frame)
        search_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        tk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT, padx=(20, 0))

        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=(3, 5))


        search_btn = ttk.Button(
            search_frame,
            text="Найти",
            command=self.search_by_substr,
            width=8
        )
        search_btn.pack(side=tk.LEFT)

        revert_btn = ttk.Button(
            search_frame,
            text="Сброс",
            command=lambda: [self.update_words_table(self.words_data),
                             self.search_entry.delete(0, tk.END)],
            width=8
        )
        revert_btn.pack(side=tk.LEFT, padx=5)

        concordance_btn = ttk.Button(
            search_frame,
            text="Показать конкорданс",
            command=self.concordance_search,
            width=25
        )
        concordance_btn.pack(side=tk.LEFT, padx=10)

        table_frame = tk.Frame(self.right_panel, padx=5,
            pady=5)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.create_words_table()

    def create_words_table(self):
        """Создаем таблицу для отображения статистики слов"""
        columns = ("word", "count", "lemma", "pos", "morph")
        table_container = tk.Frame(self.right_panel)
        table_container.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        self.word_table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            height=17,
            selectmode="browse"
        )

        self.word_table.heading("word", text="Словоформа")
        self.word_table.heading("count", text="Частота")
        self.word_table.heading("lemma", text="Лемма")
        self.word_table.heading("pos", text="Часть речи")
        self.word_table.heading("morph", text="Морфологическая информация")

        self.word_table.column("word", width=60, anchor=tk.W)
        self.word_table.column("count", width=20, anchor=tk.CENTER)
        self.word_table.column("lemma", width=60, anchor=tk.W)
        self.word_table.column("pos", width=80, anchor=tk.W)
        self.word_table.column("morph", width=410, anchor=tk.W)

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.word_table.yview)
        self.word_table.configure(yscrollcommand=scrollbar.set)

        self.word_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_texts_table(self):
        table_frame = tk.Frame(self.main_panel)
        self.main_panel.add(table_frame, width=250)

        self.tree = ttk.Treeview(table_frame, columns=("Name",), show="headings")

        self.tree.heading("Name", text="Заголовки текстов")
        self.tree.column("Name", width=230)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.add_titles()

        self.tree.bind("<<TreeviewSelect>>", self.on_text_select)

    def add_titles(self):
        response = requests.get(
            f"http://127.0.0.1:8000/texts"
        )
        response.raise_for_status()
        data = response.json()
        self.texts_data = data.get('data', {})
        for row in self.texts_data:
            self.tree.insert('', tk.END, values=row.get('title', ''))



    def filter_by_criteria(self, event=None):
        criteria = str(self.part_of_speech.get())
        filtered_words = []
        if criteria:
            for row in self.words_data:
                if row.get('part_of_speech', '') == criteria:
                    filtered_words.append(row)
            self.update_words_table(filtered_words)

    def search_by_substr(self):
        """Поиск по подстроке"""
        search_term = self.search_entry.get()
        if not search_term:
            return

        searched_data = [row for row in self.words_data if search_term in row.get('word', '').lower()]
        self.update_words_table(searched_data)


        content = self.text_info.get(1.0, tk.END)
        if search_term in content:
            self.text_info.tag_remove("highlight", 1.0, tk.END)

            # подсветка вхождений
            start = "1.0"
            while True:
                start = self.text_info.search(search_term, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(search_term)}c"
                self.text_info.tag_add("highlight", start, end)
                start = end

            self.text_info.tag_config("highlight", background="LightSeaGreen")
            # self.text_info.see(start)
        else:
            messagebox.showinfo("Поиск", f"Подстрока '{search_term}' не найдена")

    def concordance_search(self):
        search_term = self.search_entry.get()
        print(search_term)
        if not search_term:
            return
        searched_data = [row for row in self.words_data if search_term == row.get('word', '').lower()]
        if not bool(searched_data):
            messagebox.showinfo("Поиск", f"Конкорданс для слова {search_term} не найден. Пожалуйста, "
                                         f"попробуйте ввести целое слово")
        response_concordance = requests.get(
            f"http://127.0.0.1:8000/concordances/{search_term}"
        )
        response_concordance.raise_for_status()
        data = response_concordance.json()
        self.concordances = data.get('data', {})
        print(self.concordances)
        concoradnce_view = ConcordanceView(self, search_term, self.concordances)


    def update_words_table(self, searched_words):
        for item in self.word_table.get_children(''):
            self.word_table.delete(item)
        if searched_words:
            for word in searched_words:
                self.word_table.insert("", tk.END, values=(word.get('word', ''), word.get('frequency', ''),
                                                           word.get('lemma', ''), word.get('part_of_speech', ''),
                                                           word.get('feats', '')))
        else: messagebox.showinfo("Поиск", f"Не удалось обновить таблицу. Возможно,"
                                           f" выбранного критерия нет в списке")


    def start_editing(self, event=None):
        """Активация редактирования по клику"""
        if not self.selected_text:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите текст.")
            return

        if self.text_info.cget('state') == tk.DISABLED:
            self.text_info.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
            self.text_info.focus_set()

    def save_text(self):
        """Сохранение изменений в файл"""
        try:
            content = self.text_info.get(1.0, tk.END)
            url = 'http://127.0.0.1:8000/texts/update_concrete_text/'
            params = {
                "text_id": int(self.selected_text.get('id', '')),
                "new_content": content,
                "new_title": None
            }
            response = requests.post(url, json=params)
            print(response.json())
            response_words = requests.get(
                f"http://127.0.0.1:8000/words/{self.selected_text.get('id', '')}"
            )
            response_words.raise_for_status()
            data2 = response_words.json()
            self.words_data = data2.get('data', {})
            # print(self.words_data)
            self.update_words_table(self.words_data)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить текст:\n{str(e)}")

    def add_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=(("Все файлы", "*.*"), ("Текстовые файлы", "*.txt"))
        )

        if file_path:
            print(file_path)
            full_filename = os.path.basename(file_path)
            filename_without_extension = os.path.splitext(full_filename)[0]
            print(filename_without_extension)

            url = f'http://127.0.0.1:8000/texts/upload_file/{filename_without_extension}'
            params = {
                "file_path": file_path,
                "title": filename_without_extension
            }
            response = requests.post(url, params=params)
            self.add_titles()



    def on_text_select(self, event):
        if self.text_info.get("1.0", tk.END):
            if self.text_info.cget('state') == tk.DISABLED:
                self.text_info.config(state=tk.NORMAL)
            self.text_info.delete("1.0", tk.END)
        selected_item = self.tree.focus()
        if selected_item:
            title = self.tree.item(selected_item)["values"][0]
            print(title)
            self.selected_text = None
            for row in self.texts_data:
                if row.get('title', '') == title:
                    self.selected_text = row
            response = requests.get(
                f"http://127.0.0.1:8000/texts/concrete_text?text_id={self.selected_text.get('id', '')}"
            )
            response.raise_for_status()
            data = response.json()
            self.text_data = data.get('data', {})
            # print(f"text_data: {self.text_data}")
            self.text_info.insert( tk.END, self.text_data.get('content', ''))
            self.text_info.config(state=tk.DISABLED)
            response_words = requests.get(
                f"http://127.0.0.1:8000/words/{self.selected_text.get('id', '')}"
            )
            response_words.raise_for_status()
            data2 = response_words.json()
            self.words_data = data2.get('data', {})
            # print(self.words_data)
            self.update_words_table(self.words_data)
    def update_text_info(self, file_path):
        """Обновление информации о файле"""
        self.current_file_path = file_path
        self.text_info.config(state=tk.NORMAL)
        self.text_info.delete(1.0, tk.END)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.text_info.insert(tk.END, content)
        except Exception as e:
            self.text_info.insert(tk.END, f"Ошибка чтения файла: {str(e)}")

        self.text_info.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = CorpusManagerView(root)
    root.mainloop()
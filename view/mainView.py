import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox, scrolledtext
from parsingView import ParsingView
import os

import requests


class TextAnalyserView(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Синтаксический анализ текстов")
        self.geometry("1200x700")
        self.selected_text = None
        self.concordances = None

        self.create_menu()

        self.main_panel = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_panel.pack(fill=tk.BOTH, expand=True)

        self.create_texts_table()

        self.right_panel = tk.Frame(self.main_panel, bg="#f0f0f0", padx=10, pady=10)
        self.main_panel.add(self.right_panel)
        self.current_text_id: int = 0
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
            state='disabled'
        )
        self.text_info.pack(fill=tk.BOTH, expand=False)

        self.text_info.bind("<Button-1>", self.start_editing)

        self.save_button = tk.Button(
            info_frame,
            text="Сохранить",
            command=self.update_text,
            state=tk.DISABLED
        )
        self.save_button.pack(pady=5, anchor='e')



        self.create_words_table()

    def create_words_table(self):
        """Создаем таблицу для отображения статистики слов"""
        columns = ("sentences",)
        table_container = tk.Frame(self.right_panel)
        table_container.pack(fill=tk.BOTH, expand=True, pady=(2, 5))

        self.word_table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            height=17,
            selectmode="browse"
        )

        self.word_table.heading("sentences", text="Предложения")

        self.word_table.column("sentences", width=630, anchor=tk.W)

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.word_table.yview)
        self.word_table.configure(yscrollcommand=scrollbar.set)

        self.word_table.pack(side="left", fill="both", expand=True, padx=(5, 2))
        scrollbar.pack(side="right", fill="y", padx=5)

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
        self.tree.delete(*self.tree.get_children())
        # response = requests.get(
        #     f"http://127.0.0.1:8000/texts"
        # )
        # response.raise_for_status()
        # data = response.json()
        # texts_data = data.get('data', {})
        # for row in texts_data:
        #     self.tree.insert('', tk.END, values=(row['title'],), iid=row['id'])


    def start_editing(self, event=None):
        if self.text_info.cget('state') == tk.DISABLED:
            self.text_info.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
            self.text_info.focus_set()

    def update_text(self):
        try:
            content = self.text_info.get(1.0, tk.END)
            parsing_view = ParsingView(self, 'hello')
            # url = 'http://127.0.0.1:8000/texts/update_concrete_text/'
            # params = {
            #     "text_id": self.current_text_id,
            #     "new_content": content,
            #     "new_title": None
            # }
            # requests.post(url, json=params)
            # self.pull_all_words()

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

            # url = f'http://127.0.0.1:8000/texts/upload_file/{filename_without_extension}'
            # params = {
            #     "file_path": file_path,
            #     "title": filename_without_extension
            # }
            # response = requests.post(url, params=params)
            # self.add_titles()

    def on_text_select(self, event):

        if self.text_info.get("1.0", tk.END):
            if self.text_info.cget('state') == tk.DISABLED:
                self.text_info.config(state=tk.NORMAL)
            self.text_info.delete("1.0", tk.END)
        self.current_text_id = self.tree.focus()
        # if self.current_text_id:
        #     response = requests.get(
        #         f"http://127.0.0.1:8000/texts/concrete_text?text_id={self.current_text_id}"
        #     )
        #     response.raise_for_status()
        #     text_data = response.json()['data']
        #     self.text_info.insert(tk.END, text_data['content'])
        #     self.text_info.config(state=tk.DISABLED)
        #     self.pull_all_words()

    def pull_all_words(self):
        pass
        # response_words = requests.get(
        #     f"http://127.0.0.1:8000/words/{self.current_text_id}"
        # )
        # response_words.raise_for_status()
        # words = response_words.json()
        # self.update_words_table(words['data'])


if __name__ == "__main__":
    root = tk.Tk()
    app = TextAnalyserView(root)
    root.mainloop()
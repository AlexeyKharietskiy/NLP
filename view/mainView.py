import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox, scrolledtext

from logger import logger
from ParsingView import ParsingView
import os

import requests


class TextAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Семантико-синтаксический анализ текстов")
        self.geometry("1200x700")

        self.create_menu()

        self.main_panel = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_panel.pack(fill=tk.BOTH, expand=True)

        self.create_texts_table()

        self.right_panel = tk.Frame(self.main_panel, bg="#f0f0f0", padx=10, pady=10)
        self.main_panel.add(self.right_panel)

        self.current_text_id: int = 0

        self.create_right_panel()
        self.create_sentences_table()

    def create_menu(self):
        """Create window menu
        """
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Добавить файл", command=self.add_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)

        menubar.add_cascade(label="Файл", menu=file_menu)
        self.config(menu=menubar)

    def create_right_panel(self):
        self.right_panel = tk.Frame(self.main_panel, bg="#f0f0f0", padx=5, pady=5)
        self.main_panel.add(self.right_panel)
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
        self.create_text_form(info_frame)
        self.create_update_button(info_frame)
        self.create_save_button(info_frame)

    def create_text_form(self, frame: tk.Frame):
        """Create text form
        """
        self.text_info = scrolledtext.ScrolledText(
            frame,
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

    def create_save_button(self, frame: tk.LabelFrame):
        convert_info_button = tk.Button(
            frame,
            text="Сохранить",
            command=self.save_text,
        )
        convert_info_button.pack(side=tk.LEFT, padx=(0, 5))

    def create_update_button(self, frame: tk.LabelFrame):
        self.update_button = tk.Button(
            frame,
            text="Обновить",
            command=self.update_text,
            state=tk.DISABLED
        )
        self.update_button.pack(side=tk.RIGHT)

    def create_sentences_table(self):
        table_container = tk.Frame(self.right_panel)
        table_container.pack(fill=tk.BOTH, expand=True, pady=(2, 5))

        self.sentence_listbox = tk.Listbox(
            table_container,
            height=17,
            selectmode=tk.SINGLE,
            font=('Arial', 10),
            relief=tk.FLAT,
            activestyle='none'
        )
        v_scroll = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.sentence_listbox.yview
        )
        self.sentence_listbox.configure(yscrollcommand=v_scroll.set)

        h_scroll = ttk.Scrollbar(
            table_container,
            orient="horizontal",
            command=self.sentence_listbox.xview
        )
        self.sentence_listbox.configure(xscrollcommand=h_scroll.set)
        self.sentence_listbox.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        self.sentence_listbox.bind("<Double-ButtonPress-1>", self.on_sentence_click)

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
        self.update_titles()

        self.tree.bind("<<TreeviewSelect>>", self.on_text_select)

    def update_titles(self):
        self.tree.delete(*self.tree.get_children())
        response = requests.get(
            f"http://127.0.0.1:8000/texts/text_titles"
        )
        if response.status_code == 404:
            error_data = response.json()
            logger.error(f"{error_data.get('detail')}")
        else:
            data = response.json()
            titles = data.get('data', {})
            for row in titles:
                self.tree.insert('', tk.END, values=(row['title'],), iid=row['id'])

    def start_editing(self, event=None):
        if self.text_info.cget('state') == tk.DISABLED:
            self.text_info.config(state=tk.NORMAL)
            self.update_button.config(state=tk.NORMAL)
            self.text_info.focus_set()

    def update_text(self):
        content = self.text_info.get(1.0, tk.END)
        url = f'http://127.0.0.1:8000//texts/new_content/{self.current_text_id}'
        params = {
            "new_content": content,
        }
        response = requests.patch(url, json=params)
        if response.status_code == 404:
            error_data = response.json()
            logger.error(f"{error_data.get('detail')}")
        else:
            self.fill_in_all_sentences()

    def add_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=(
                ("Текстовые файлы", "*.txt"),
                ("DOCX", "*.docx*"),
                ("PDF", "*.pdf*"),
            )
        )
        if file_path:
            full_filename = os.path.basename(file_path)
            filename_without_extension = os.path.splitext(full_filename)[0]

            url = f'http://127.0.0.1:8000/texts/upload_file'
            params = {
                "file_path": file_path,
                "title": filename_without_extension
            }
            response = requests.post(url=url, json=params)
            if response.status_code == 404:
                error_data = response.json()
                logger.error(f"{error_data.get('detail')}")
            else:
                logger.info(f"Add file with title '{filename_without_extension}'")
                logger.info(f"Details: {response.json().get('detail')}")

                self.update_titles()

    def on_text_select(self, event):

        if self.text_info.get("1.0", tk.END):
            if self.text_info.cget('state') == tk.DISABLED:
                self.text_info.config(state=tk.NORMAL)
            self.text_info.delete("1.0", tk.END)
        self.current_text_id = self.tree.focus()
        if self.current_text_id:
            response = requests.get(
                f"http://127.0.0.1:8000/texts/concrete_text/{self.current_text_id}"
            )
            if response.status_code == 404:
                error_data = response.json()
                logger.error(f"{error_data.get('detail')}")
            else:
                text_data = response.json()['data']
                self.text_info.insert(tk.END, text_data['content'])
                self.text_info.config(state=tk.DISABLED)
                self.fill_in_all_sentences()

    def fill_in_all_sentences(self):
        response = requests.get(
            f"http://127.0.0.1:8000/sentences/{self.current_text_id}"
        )
        if response.status_code == 404:
            error_data = response.json()
            logger.error(f"{error_data.get('detail')}")
        else:
            sentences = response.json()
            self.update_sentence_table(sentences['data'])

    def update_sentence_table(self, searched_sentences):
        """Обновляем список предложений"""
        self.sentence_listbox.delete(0, tk.END)

        if searched_sentences:
            self.sentences_data = searched_sentences
            [
                self.sentence_listbox.insert(tk.END, sent['sentence'])
                for sent in searched_sentences
            ]

    def on_sentence_click(self, event):
        """Обработчик выбора предложения"""
        if not self.sentence_listbox.curselection():
            return

        index = self.sentence_listbox.curselection()[0]
        selected_sentence = self.sentences_data[index]
        ParsingView(self, selected_sentence['id'])

    def save_text(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")]
        )
        if file_path:
            url = f"http://127.0.0.1:8000/texts/save/{self.current_text_id}"
            params = {"filepath": file_path}
            response = requests.post(url=url, json=params)
            if response.status_code == 404:
                error_data = response.json()
                logger.error(f"{error_data.get('detail')}")
            else:
                logger.info(f"Save file with id {self.current_text_id} into {file_path}")

    def run(self):
        self.mainloop()
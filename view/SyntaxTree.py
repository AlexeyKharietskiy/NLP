import tkinter as tk
from random import randint

import requests

class SyntaxTreeApp:
    def __init__(self, root, sentence_id):
        self.root = root
        self.sentence_id = sentence_id
        self.tokens = None

        # Получаем данные с сервера
        self.fetch_data()

        # Создаем Canvas
        self.canvas = tk.Canvas(self.root, width=1200, height=500, bg="white", scrollregion=(0, 0, 2000, 600))
        hbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        hbar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=hbar.set)
        self.canvas.pack()

        # Словари для хранения позиций
        self.word_positions = {}  # Позиции слов
        self.levels = {}  # Уровни зависимостей

        # Вычисляем позиции слов и уровни
        self.calculate_positions()
        self.calculate_levels()

        # Рисуем дерево
        self.draw_tree()

    def fetch_data(self):
        # Выполняем HTTP-запрос к серверу
        url = f"http://127.0.0.1:8000/words/{self.sentence_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем, успешен ли запрос
            self.tokens = response.json()['data']
            print("Полученные данные с сервера:", self.tokens)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе данных: {e}")
            self.tokens = []

    def calculate_positions(self):
        # Вычисляем позиции слов внизу
        x_offset = 20
        y_text = 400
        for token in self.tokens:
            word_width = len(token["word"]) * 10
            self.word_positions[token["id"]] = (x_offset + word_width // 2, y_text)
            x_offset += word_width + 15

    def calculate_levels(self):
        # Определяем уровни зависимостей (глубина от корня)
        root = None
        for token in self.tokens:
            if  "сказуемое" in token["relation"]:
                root = token
                break

        if not root:
            for token in self.tokens:
                if token["relation"] == "подлежащее":
                    root = token
                    print("Найдено только подлежащее")
                    break
        if not root:
            print("Корень предложения не найден")
            return

        print(f"Корень предложения: {root['word']} (id: {root['id']})")

        for token in self.tokens:
            current = token
            level_count = 0
            while current["id"] != root["id"]:
                # Ищем родителя по значению head (слово-родитель)
                parent = None
                for t in self.tokens:
                    if t["word"] == current["head"]:
                        if t['head'] == current["word"]:
                            level_count += 1
                            continue
                        parent = t
                        break
                if not parent:
                    print(f"Родитель для слова '{current['word']}' (head: '{current['head']}') не найден")
                    break
                current = parent
                level_count += 1
            self.levels[token["id"]] = level_count
        print("Уровни зависимостей:", self.levels)

    def draw_tree(self):
        # Очищаем Canvas
        self.canvas.delete("all")

        if not self.tokens:
            self.canvas.create_text(600, 300, text="Не удалось загрузить данные", font=("Arial", 12))
            return

        # Рисуем слова и POS-теги (POS-тегов пока нет)
        for token in self.tokens:
            x, y = self.word_positions[token["id"]]
            word_width = len(token["word"]) * 10
            x_start = x - word_width // 2

            # Рисуем слово
            self.canvas.create_text(x, y, text=token["word"], font=("Arial", 12))

            # Рисуем POS-тег (пока пусто, можно добавить позже)
            self.canvas.create_text(x, y + 30, text="", font=("Arial", 10))

            # Рисуем подчеркивания
            y_underline = y + 15
            if token["relation"] == "подлежащее":  # Подлежащее - сплошная линия
                self.canvas.create_line(x_start, y_underline, x_start + word_width, y_underline, fill="black")

            elif "сказуемое" in token["relation"] or token["relation"] == 'дополнительное предложение'\
                    or token["relation"] == 'обстоятельственное предложение'\
                    or token["relation"] == 'относительное предложение'\
                    or token["relation"] == 'определительное предложение'\
                    or token["relation"] == "предикативное придаточное":  # Сказуемое - двойная линия
                self.canvas.create_line(x_start, y_underline, x_start + word_width, y_underline, fill="black")
                self.canvas.create_line(x_start, y_underline + 3, x_start + word_width, y_underline + 3, fill="black")

            elif (token["relation"] == 'согласованное определение' or
                  token["relation"] == 'несогласованное определение' or
                  token["relation"] == 'притяжательное определение' or
                  token["relation"] == 'агентивное определение' or
                  token["relation"] == 'определитель'):
                points = []
                for i in range(0, word_width + 1, 5):
                    x_point = x_start + i
                    y_point = y_underline + (3 if i % 10 == 0 else -3)
                    points.extend([x_point, y_point])
                self.canvas.create_line(*points, fill="black", smooth=True)

            elif (token["relation"] == 'прямое дополнение' or
                  token["relation"] =='косвенное дополнение' or
                  token["relation"] =='агентивное дополнение' or
                  token["relation"] =='предикативное дополнение' or
                  token["relation"] == 'глагольное дополнение'):  # Прямое дополнение - пунктирная линия
                dash_pattern = (4, 4)  # Пунктир
                self.canvas.create_line(x_start, y_underline, x_start + word_width, y_underline, dash=dash_pattern,
                                        fill="black")

            elif (token["relation"] == 'обстоятельственное придаточное'
                or token["relation"] == "обстоятельство"
                or token["relation"] == 'временное обстоятельство'):  # Предлог - точечная линия
                dash_pattern = (2, 4)  # Точечная линия
                self.canvas.create_line(x_start, y_underline, x_start + word_width, y_underline, dash=(25, 5, 1, 10), fill="black")

        # Рисуем зависимости с прямыми углами и стрелками
        y_base = 350  # Базовая высота для первого уровня
        level_height = 30  # Расстояние между уровнями

        # Инициализируем словари для отслеживания
        self.label_positions = {}  # Для меток
        self.line_positions = {}  # Для линий на каждом уровне
        parent_connections = {}  # Для отслеживания количества подключений к родителям

        # Создаем список зависимостей и сортируем их по X-координате дочернего слова
        dependencies = []
        for token in self.tokens:
            if token["relation"] == "сказуемое":
                continue
            elif token['relation'] == "подлежащее":
                continue
            x_token, _ = self.word_positions[token["id"]]
            dependencies.append((token, x_token))

        # Сортируем зависимости по X-координате дочернего слова
        dependencies.sort(key=lambda x: x[1])

        for token, x_token in dependencies:
            # Позиция текущего слова
            x_token, y_token = self.word_positions[token["id"]]

            # Позиция родителя
            parent = None
            for t in self.tokens:
                if t["word"] == token["head"]:
                    parent = t
                    break
            if not parent:
                print(f"Не найден родитель для слова '{token['word']}' (head: '{token['head']}')")
                continue

            x_parent, y_parent = self.word_positions[parent["id"]]

            # Уровень зависимости
            if token["id"] not in self.levels:
                print(f"Уровень зависимости для слова '{token['word']}' не рассчитан")
                continue
            level = self.levels[token["id"]]
            y_level = y_base - level * level_height

            if parent["id"] not in parent_connections:
                parent_connections[parent["id"]] = 0
            parent_connections[parent["id"]] += 1

            x_offset = (parent_connections[parent["id"]] - 1) * 5
            max_x_offset = 30
            x_offset = min(x_offset, max_x_offset)
            adjusted_x_parent = x_parent + x_offset

            # Проверяем пересечения линий на этом уровне
            if level not in self.line_positions:
                self.line_positions[level] = []

            # Определяем X-диапазон текущей линии
            x_start = min(x_token, x_parent)
            x_end = max(x_token, x_parent)

            # Сохраняем информацию о текущей линии
            self.line_positions[level].append((x_start, x_end, x_end))

            color = "#" + "%06x" % randint(0, 0xFFFFFF)

            # Рисуем линию с прямыми углами
            # Вертикальная линия от слова
            self.canvas.create_line(x_token - 5, y_token - 10, x_token - 5 , y_level, fill=color)

            # Горизонтальная линия от дочернего слова к родителю
            self.canvas.create_line(x_token - 5, y_level, adjusted_x_parent, y_level, fill=color)

            # Вертикальная линия к родителю
            self.canvas.create_line(adjusted_x_parent, y_level, adjusted_x_parent, y_parent - 5, fill=color)
            # Рисуем стрелку
            self.canvas.create_line(
                x_token - 5, y_base + 20,  # Левая точка стрелки
                x_token - 5, y_base + 45,      # Вершина стрелки
                arrow=tk.LAST, # Стрелка на конце
                fill=color            )

            label_x = (x_token + x_parent) // 2
            label_y = y_level - 15

            # счетчик меток на этом уровне
            if level not in self.label_positions:
                self.label_positions[level] = {"count": 0}
            self.label_positions[level]["count"] += 1

            offset = (self.label_positions[level]["count"] - 1) * 10

            max_offset = 100
            offset = min(offset, max_offset)
            adjusted_label_y = label_y + offset

            # лог координаты метки
            print(f"Метка '{token['relation'].upper()}': x={label_x}, y={adjusted_label_y}, offset={offset}")

            label_text = token["relation"].upper()
            font_size = 7 if len(label_text) <= 15 else 5  # Уменьшаем шрифт для длинных меток

            temp_label = self.canvas.create_text(
                label_x, adjusted_label_y,
                text=label_text,
                font=("Arial", font_size),
                fill="black"
            )
            bbox = self.canvas.bbox(temp_label)
            self.canvas.create_rectangle(
                bbox,
                fill="white",
                outline="white"
            )

            self.canvas.create_text(
                label_x, adjusted_label_y,
                text=label_text,
                font=("Arial", font_size),
                fill="black"
            )
            self.canvas.delete(temp_label)



class App:
    def __init__(self, sentence_id):
        self.sentence_id = sentence_id
        self.root = tk.Tk()
        self.root.title("Syntax Tree Visualizer")

        # Инициализация приложения
        self.draw()

    def draw(self):
        if not self.sentence_id:
            return
        # Удаляем предыдущее дерево, если оно есть
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
        # Создаем новое дерево
        SyntaxTreeApp(self.root, self.sentence_id)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App(135)
    app.run()
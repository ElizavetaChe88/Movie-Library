import json
import os
from tkinter import *
from tkinter import ttk, messagebox

DATA_FILE = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("800x500")
        self.root.resizable(True, True)

        # Данные
        self.movies = []
        self.load_data()

        # GUI элементы
        self.create_input_frame()
        self.create_table()
        self.create_filter_frame()

        # Обновить таблицу
        self.refresh_table()

    def create_input_frame(self):
        """Форма для ввода нового фильма"""
        input_frame = LabelFrame(self.root, text="Добавить фильм", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Название
        Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.title_entry = Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        # Жанр
        Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.genre_entry = Entry(input_frame, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=2)

        # Год
        Label(input_frame, text="Год выпуска:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.year_entry = Entry(input_frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Рейтинг
        Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.rating_entry = Entry(input_frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        # Кнопка
        self.add_btn = Button(input_frame, text="Добавить фильм", command=self.add_movie, bg="green", fg="white")
        self.add_btn.grid(row=1, column=4, padx=10, pady=2)

    def create_table(self):
        """Таблица для отображения фильмов"""
        table_frame = Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Scrollbar
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Title", "Genre", "Year", "Rating"),
                                 show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Определяем колонки
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Year", text="Год")
        self.tree.heading("Rating", text="Рейтинг")

        self.tree.column("ID", width=40)
        self.tree.column("Title", width=200)
        self.tree.column("Genre", width=120)
        self.tree.column("Year", width=80)
        self.tree.column("Rating", width=80)

        self.tree.pack(side=LEFT, fill="both", expand=True)
        scroll_y.pack(side=RIGHT, fill="y")
        scroll_x.pack(side=BOTTOM, fill="x")

    def create_filter_frame(self):
        """Фильтрация по жанру и году"""
        filter_frame = LabelFrame(self.root, text="Фильтрация", padx=10, pady=5)
        filter_frame.pack(fill="x", padx=10, pady=5)

        Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=5, pady=2)
        self.filter_genre_entry = Entry(filter_frame, width=20)
        self.filter_genre_entry.grid(row=0, column=1, padx=5, pady=2)

        Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2, padx=5, pady=2)
        self.filter_year_entry = Entry(filter_frame, width=10)
        self.filter_year_entry.grid(row=0, column=3, padx=5, pady=2)

        Button(filter_frame, text="Применить фильтр", command=self.refresh_table).grid(row=0, column=4, padx=5)
        Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter).grid(row=0, column=5, padx=5)

    def add_movie(self):
        """Добавление фильма с валидацией"""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        # Валидация
        if not title or not genre or not year_str or not rating_str:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
            return

        try:
            year = int(year_str)
            if year < 1888 or year > 2030:
                messagebox.showerror("Ошибка", "Год должен быть между 1888 и 2030")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть целым числом!")
            return

        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return

        # ID для фильма
        new_id = max([m["id"] for m in self.movies], default=0) + 1

        self.movies.append({
            "id": new_id,
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        })

        self.save_data()
        self.clear_inputs()
        self.refresh_table()
        messagebox.showinfo("Успех", f"Фильм '{title}' добавлен!")

    def clear_inputs(self):
        self.title_entry.delete(0, END)
        self.genre_entry.delete(0, END)
        self.year_entry.delete(0, END)
        self.rating_entry.delete(0, END)

    def refresh_table(self):
        """Обновление таблицы с учетом фильтров"""
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получаем фильтры
        genre_filter = self.filter_genre_entry.get().strip().lower()
        year_filter_str = self.filter_year_entry.get().strip()

        filtered_movies = self.movies

        if genre_filter:
            filtered_movies = [m for m in filtered_movies if genre_filter in m["genre"].lower()]

        if year_filter_str:
            try:
                year_filter = int(year_filter_str)
                filtered_movies = [m for m in filtered_movies if m["year"] == year_filter]
            except ValueError:
                if year_filter_str:
                    messagebox.showwarning("Предупреждение", "Год фильтра должен быть числом")

        # Заполняем таблицу
        for movie in filtered_movies:
            self.tree.insert("", END, values=(movie["id"], movie["title"], movie["genre"],
                                              movie["year"], movie["rating"]))

    def reset_filter(self):
        self.filter_genre_entry.delete(0, END)
        self.filter_year_entry.delete(0, END)
        self.refresh_table()

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except:
                self.movies = []
        else:
            # Пример данных для демонстрации
            self.movies = [
                {"id": 1, "title": "Побег из Шоушенка", "genre": "Драма", "year": 1994, "rating": 9.3},
                {"id": 2, "title": "Криминальное чтиво", "genre": "Криминал", "year": 1994, "rating": 8.9},
                {"id": 3, "title": "Тёмный рыцарь", "genre": "Боевик", "year": 2008, "rating": 9.0},
            ]

if __name__ == "__main__":
    root = Tk()
    app = MovieLibrary(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")

        self.movies = []

        # --- Форма ---
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Название").grid(row=0, column=0)
        tk.Label(frame, text="Жанр").grid(row=1, column=0)
        tk.Label(frame, text="Год").grid(row=2, column=0)
        tk.Label(frame, text="Рейтинг").grid(row=3, column=0)

        self.title_entry = tk.Entry(frame)
        self.genre_entry = tk.Entry(frame)
        self.year_entry = tk.Entry(frame)
        self.rating_entry = tk.Entry(frame)

        self.title_entry.grid(row=0, column=1)
        self.genre_entry.grid(row=1, column=1)
        self.year_entry.grid(row=2, column=1)
        self.rating_entry.grid(row=3, column=1)

        tk.Button(frame, text="Добавить фильм", command=self.add_movie).grid(row=4, columnspan=2, pady=5)

        # --- Фильтры ---
        filter_frame = tk.Frame(root)
        filter_frame.pack()

        tk.Label(filter_frame, text="Фильтр по жанру").grid(row=0, column=0)
        self.filter_genre = tk.Entry(filter_frame)
        self.filter_genre.grid(row=0, column=1)

        tk.Label(filter_frame, text="Фильтр по году").grid(row=0, column=2)
        self.filter_year = tk.Entry(filter_frame)
        self.filter_year.grid(row=0, column=3)

        tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=0, column=4)
        tk.Button(filter_frame, text="Сброс", command=self.show_all).grid(row=0, column=5)

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("title", "genre", "year", "rating"), show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")

        self.tree.pack(pady=10)

        # загрузка данных
        self.load_data()
        self.show_all()

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        rating = self.rating_entry.get()

        # --- Проверки ---
        if not title or not genre:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        if not year.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return

        try:
            rating = float(rating)
            if rating < 0 or rating > 10:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": rating
        }

        self.movies.append(movie)
        self.save_data()
        self.show_all()

    def show_all(self):
        self.update_table(self.movies)

    def apply_filter(self):
        genre = self.filter_genre.get().lower()
        year = self.filter_year.get()

        filtered = self.movies

        if genre:
            filtered = [m for m in filtered if genre in m["genre"].lower()]

        if year.isdigit():
            filtered = [m for m in filtered if m["year"] == int(year)]

        self.update_table(filtered)

    def update_table(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for movie in data:
            self.tree.insert("", "end", values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.movies = json.load(f)
                
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()

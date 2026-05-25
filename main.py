import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Константы
FAVORITES_FILE = "favorites.json"
GITHUB_API_URL = "https://api.github.com/users/"

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("600x500")

        # Загрузка избранных пользователей
        self.favorites = self.load_favorites()

        self.setup_ui()

    def setup_ui(self):
        # Поле ввода
        tk.Label(self.root, text="Введите имя пользователя GitHub:").pack(pady=5)
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)

        # Кнопка поиска
        search_button = tk.Button(self.root, text="Найти", command=self.search_user)
        search_button.pack(pady=5)

        # Список результатов
        self.results_listbox = tk.Listbox(self.root, height=10, width=70)
        self.results_listbox.pack(pady=10)

        # Кнопки управления избранным
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        add_favorite_button = tk.Button(button_frame, text="Добавить в избранное",
                                      command=self.add_to_favorites)
        add_favorite_button.pack(side=tk.LEFT, padx=5)

        remove_favorite_button = tk.Button(button_frame, text="Удалить из избранного",
                                         command=self.remove_from_favorites)
        remove_favorite_button.pack(side=tk.LEFT, padx=5)

        # Список избранных
        tk.Label(self.root, text="Избранные пользователи:").pack(pady=5)
        self.favorites_listbox = tk.Listbox(self.root, height=10, width=70)
        self.favorites_listbox.pack(pady=10)

        self.update_favorites_list()

    def search_user(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым!")
            return

        try:
            response = requests.get(f"{GITHUB_API_URL}{username}")
            if response.status_code == 200:
                user_data = response.json()
                self.display_user(user_data)
            else:
                messagebox.showerror("Ошибка", f"Пользователь '{username}' не найден!")
        except requests.RequestException as e:
            messagebox.showerror("Ошибка сети", f"Не удалось подключиться к API: {e}")

    def display_user(self, user_data):
        self.results_listbox.delete(0, tk.END)
        user_info = f"{user_data['login']} - {user_data.get('name', 'No name')} - {user_data['public_repos']} репозиториев"
        self.results_listbox.insert(tk.END, user_info)

    def add_to_favorites(self):
        selection = self.results_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите пользователя из результатов поиска!")
            return

        user_info = self.results_listbox.get(selection[0])
        username = user_info.split(" - ")[0]

        if username not in self.favorites:
            self.favorites.append(username)
            self.save_favorites()
            self.update_favorites_list()
            messagebox.showinfo("Успех", f"{username} добавлен в избранное!")
        else:
            messagebox.showinfo("Информация", f"{username} уже в избранном!")

    def remove_from_favorites(self):
        selection = self.favorites_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите пользователя из списка избранного!")
            return

        username = self.favorites_listbox.get(selection[0])
        self.favorites.remove(username)
        self.save_favorites()
        self.update_favorites_list()
        messagebox.showinfo("Успех", f"{username} удалён из избранного!")

    def load_favorites(self):
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_favorites(self):
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=2)

    def update_favorites_list(self):
        self.favorites_listbox.delete(0, tk.END)
        for username in self.favorites:
            self.favorites_listbox.insert(tk.END, username)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
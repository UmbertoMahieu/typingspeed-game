import tkinter as tk
import csv
from tkinter import font
import time


class TypingSpeedApp:
    def __init__(self, root):
        #setup
        self.root = root
        self.root.title = "TypingSpeedApp"
        self.words_file_path = "words_list.csv"
        self.words_list = self.load_words()
        self.setup_ui()

        #variables
        self.status = False
        self.correct_words = []
        self.wrong_words = []
        self.current_word = self.words_list[0]
        self.start_game = None
        self.stop_game = None

        self.display_words()



    def setup_ui(self):

        self.canvas = tk.Canvas(self.root, bg="white", width=500, height=400)
        self.canvas.pack(fill="both", expand=True)

        big_bold_font = font.Font(family="Arial", size=36, weight="bold")
        small_gray_font = font.Font(family="Arial", size=14)

        self.current_word_label = tk.Label(self.root, text="FIRST WORD", font=big_bold_font, fg='black', bg="white")
        self.canvas.create_window(250, 150, window=self.current_word_label)

        self.next_word_label = tk.Label(self.root, text="NEXT WORD", font=small_gray_font, fg='gray', bg="white")
        self.canvas.create_window(250, 200, window=self.next_word_label)

        self.text_entry = tk.Entry(self.root, width=40)
        self.canvas.create_window(250, 325, window=self.text_entry)
        self.text_entry.bind("<space>", self.game_manager)
        self.text_entry.bind("<Return>", self.game_manager)


    def load_words(self):
        words = []
        try:
            with open(self.words_file_path, mode='r', newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    word = row.get("Word")
                    if word:
                        words.append(word.strip())
            return words
        except Exception as e:
            print(f"An error has occured : {e}")

    def game_manager(self, event):
        if self.status == False:
            self.status = True
            self.start_game = time.time()
        typed_word = self.text_entry.get().strip()
        if typed_word == self.current_word:
            self.correct_words.append(typed_word)
        else:
            self.wrong_words.append(typed_word)
        if self.current_word == self.words_list[-1]:
            self.status = False
            self.stop_game = time.time()
            self.display_result()
        else:
            self.current_word = self.words_list[self.words_list.index(self.current_word) + 1]
            self.display_words()
        self.text_entry.delete(0, tk.END)

    def display_result(self):
        game_duration = self.stop_game - self.start_game
        self.canvas.create_text(250, 225, text=f"Nombre de mots tapés correctement : {len(self.correct_words)}", font=("Ariel", 10, "italic"))
        self.canvas.create_text(250, 250, text=f"Nombre de mots tapés avec erreur : {len(self.wrong_words)}", font=("Ariel", 10, "italic"))
        self.canvas.create_text(250, 275, text=f'Temps nécessaire pour taper correctement {len(self.correct_words)} mots : {game_duration:.2f} secondes', font=("Ariel", 10, "italic"))
        self.canvas.create_text(250, 300, text=f'Nombre de mots/minutes : {len(self.correct_words)/(game_duration / 60):.2f}', font=("Ariel", 10, "italic"))
        self.start_button = tk.Button(self.root, text="Start over", command=self.start_new_game)
        self.canvas.create_window(250, 50, window=self.start_button)

    def start_new_game(self):
        for widget in root.winfo_children():
            widget.destroy()
        self.correct_words = []
        self.wrong_words = []
        self.current_word = self.words_list[0]
        self.status = False
        self.setup_ui()
        self.display_words()
        self.text_entry.delete(0, tk.END)


    def display_words(self):
        self.current_word_label.config(text=self.current_word)
        if self.current_word == self.words_list[-1]:
            self.next_word_label.config(text="")
        else:
            self.next_word_label.config(text=self.words_list[self.words_list.index(self.current_word) + 1])


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedApp(root)
    root.mainloop()
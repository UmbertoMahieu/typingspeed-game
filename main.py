import tkinter as tk
import csv
from tkinter import font


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
        self.canvas.create_window(250, 300, window=self.text_entry)
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
        typed_word = self.text_entry.get().strip()
        if typed_word == self.current_word:
            self.correct_words.append(typed_word)
        else:
            self.wrong_words.append(typed_word)
        self.current_word = self.words_list[self.words_list.index(self.current_word) + 1]
        self.display_words()
        self.text_entry.delete(0, tk.END)

    def display_words(self):
        self.current_word_label.config(text=self.current_word)
        self.next_word_label.config(text=self.words_list[self.words_list.index(self.current_word) + 1])


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedApp(root)
    root.mainloop()
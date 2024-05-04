import tkinter as tk
import random

class WordScrambleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Scramble")

        self.words = ["PYTHON", "PROGRAMMING", "COMPUTER", "PYTHONIC", "DEVELOPER", "CODING"]
        self.word = random.choice(self.words)
        self.scrambled_word = self.scramble_word(self.word)

        self.word_label = tk.Label(root, text=self.scrambled_word, font=("Helvetica", 24))
        self.word_label.pack(pady=10)

        self.guess_entry = tk.Entry(root, font=("Helvetica", 18))
        self.guess_entry.pack(pady=5)

        self.guess_button = tk.Button(root, text="Guess", command=self.check_guess)
        self.guess_button.pack(pady=5)

        self.message_label = tk.Label(root, text="")
        self.message_label.pack(pady=5)

    def scramble_word(self, word):
        word_list = list(word)
        random.shuffle(word_list)
        return ''.join(word_list)

    def check_guess(self):
        guess = self.guess_entry.get().strip().upper()
        self.guess_entry.delete(0, tk.END)

        if guess == self.word:
            self.message_label.config(text="Correct! You guessed the word!")
        else:
            self.message_label.config(text="Incorrect guess. Try again.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WordScrambleGame(root)
    root.mainloop()

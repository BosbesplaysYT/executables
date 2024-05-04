import tkinter as tk
import random

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")

        self.words = ["hangman", "python", "computer", "programming", "game", "code"]

        self.word = random.choice(self.words)
        self.remaining_guesses = 6
        self.guessed_letters = set()

        self.word_display = tk.StringVar()
        self.word_display.set("_ " * len(self.word))
        self.word_label = tk.Label(root, textvariable=self.word_display, font=("Arial", 20))
        self.word_label.pack(pady=20)

        self.guess_entry = tk.Entry(root, font=("Arial", 16))
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind("<Return>", self.check_guess)

        self.message_label = tk.Label(root, text="", font=("Arial", 16))
        self.message_label.pack(pady=10)

    def check_guess(self, event):
        if self.remaining_guesses <= 0:
            self.message_label.config(text="Game over. You ran out of guesses.")
            self.guess_entry.config(state=tk.DISABLED)
            return

        guess = self.guess_entry.get().lower()

        if len(guess) != 1 or not guess.isalpha():
            self.message_label.config(text="Please enter a single letter.")
            self.guess_entry.delete(0, tk.END)
            return

        if guess in self.guessed_letters:
            self.message_label.config(text="You already guessed that letter.")
            self.guess_entry.delete(0, tk.END)
            return

        self.guessed_letters.add(guess)

        if guess not in self.word:
            self.remaining_guesses -= 1
            self.message_label.config(text=f"Wrong guess. {self.remaining_guesses} guesses left.")
        else:
            word_display_list = list(self.word_display.get())
            for i, letter in enumerate(self.word):
                if letter == guess:
                    word_display_list[i * 2] = guess
            self.word_display.set(" ".join(word_display_list))

        self.check_win_or_loss()

        self.guess_entry.delete(0, tk.END)

    def check_win_or_loss(self):
        if "_" not in self.word_display.get():
            self.message_label.config(text="Congratulations! You guessed the word.")
            self.guess_entry.config(state=tk.DISABLED)
        elif self.remaining_guesses <= 0:
            self.message_label.config(text=f"Game over. The word was '{self.word}'.")
            self.guess_entry.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGame(root)
    root.mainloop()

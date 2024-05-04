import tkinter as tk
from tkinter import messagebox
import random
import pygame
import sys

class NumberGuessingGame:
    def __init__(self, master, mode, time_setting, button_click_sound):
        self.master = master
        self.master.title("Nummer Raden Spel")
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg="#f0f0f0")
        
        # Initialize Pygame mixer for playing music and sound effects
        pygame.mixer.init()

        # Load background music
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.play(-1)  # Loop indefinitely

        # Load button click sound effect
        self.button_click_sound = button_click_sound

        self.mode = mode
        self.secret_number = random.randint(1, 100)
        self.attempts = 0

        # Read time setting from settings.txt
        self.time_setting = self.read_time_setting(time_setting)
        
        if self.mode == "medium":
            self.tries_left = 10
            self.info_label = tk.Label(master, text=f"Resterende pogingen: {self.tries_left}", font=("Helvetica", 14), bg="#f0f0f0")
            self.info_label.pack()
        elif self.mode == "hard":
            self.tries_left = 10
            self.info_label = tk.Label(master, text=f"Resterende pogingen: {self.tries_left}", font=("Helvetica", 14), bg="#f0f0f0")
            self.info_label.pack()
            self.time_left = self.time_setting
            self.time_label = tk.Label(master, text=f"Resterende tijd: {self.time_left}", font=("Helvetica", 14), bg="#f0f0f0")
            self.time_label.pack()
            self.timer()

        self.title_label = tk.Label(master, text="Nummer Raden Spel", font=("Helvetica", 20), bg="#f0f0f0")
        self.title_label.pack(pady=20)
        
        self.instruction_label = tk.Label(master, text="Voer een nummer tussen 1 en 100 in:", font=("Helvetica", 14), bg="#f0f0f0")
        self.instruction_label.pack()
        
        self.guess_entry = tk.Entry(master, font=("Helvetica", 14))
        self.guess_entry.pack(pady=5)
        self.guess_entry.focus()
        
        self.guess_button = tk.Button(master, text="Gok", font=("Helvetica", 14), command=self.check_guess, bg="#4CAF50", fg="white", relief="raised")
        self.guess_button.pack(pady=5)
        self.guess_button.bind("<Button-1>", lambda event: self.play_button_click_sound())  # Bind click event

        self.master.bind("<Return>", self.check_guess)
        self.master.bind("<Escape>", lambda e: self.master.quit())

    def play_button_click_sound(self):
        self.button_click_sound.play()

    def check_guess(self, event=None):
        try:
            guess = int(self.guess_entry.get())
            if guess <= 0 or guess > 100:
                messagebox.showerror("Ongeldig Nummer", "Voer a.u.b. een nummer tussen 1 en 100 in.")
                self.guess_entry.delete(0, tk.END)
                return

            self.attempts += 1
            
            if guess == self.secret_number:
                # Play correct guess sound effect
                self.play_sound_effect("correct_guess.mp3")
                self.show_end_screen("Gefeliciteerd!", f"Je hebt het nummer {self.secret_number} geraden in {self.attempts} pogingen!")
            elif guess < self.secret_number:
                # Play lower guess sound effect
                self.play_sound_effect("lower_guess.mp3")
                messagebox.showinfo("Probeer Opnieuw", "Probeer hoger te gokken!")
            else:
                # Play higher guess sound effect
                self.play_sound_effect("lower_guess.mp3")
                messagebox.showinfo("Probeer Opnieuw", "Probeer lager te gokken!")
            
            if self.mode != "infinite":
                self.tries_left -= 1
                self.info_label.config(text=f"Resterende pogingen: {self.tries_left}")
                
                if self.tries_left == 0:
                    self.show_end_screen("Spel Voorbij", f"Het geheime nummer was {self.secret_number}. Je hebt alle pogingen opgebruikt.")
            
            self.guess_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Fout", "Voer a.u.b. een geldig nummer in.")
            self.guess_entry.delete(0, tk.END)

    def timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Resterende tijd: {self.time_left}")
            self.master.after(1000, self.timer)
        else:
            self.show_end_screen("Tijd is Op", "Je hebt geen tijd meer.")

    def show_end_screen(self, title, message):
        if self.mode == "hard":
            self.master.after_cancel(self.timer)
        
        end_screen = tk.Toplevel(self.master)
        end_screen.title(title)
        end_screen.attributes('-fullscreen', True)
        
        end_label = tk.Label(end_screen, text=message, font=("Helvetica", 14))
        end_label.pack(pady=20)
        
        close_button = tk.Button(end_screen, text="Terug naar menu", font=("Helvetica", 14), command=self.return_to_main_menu)
        close_button.pack(pady=10)

    def return_to_main_menu(self):
        self.master.destroy()
        root = tk.Tk()
        start_screen = StartScreen(root)
        root.mainloop()

    def play_sound_effect(self, sound_file):
        sound = pygame.mixer.Sound(sound_file)
        sound.play()

    def read_time_setting(self, time_setting):
        if time_setting.startswith("time"):
            return int(time_setting[4:])  # Remove "time" prefix
        else:
            return 30  # Default time setting if prefix is missing


class StartScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Nummer Raden Spel")
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg="#f0f0f0")
        
        self.title_label = tk.Label(master, text="Nummer Raden Spel", font=("Helvetica", 20), bg="#f0f0f0")
        self.title_label.pack(pady=20)
        
        self.start_label = tk.Label(master, text="Selecteer Moeilijkheidsgraad:", font=("Helvetica", 16), bg="#f0f0f0")
        self.start_label.pack()
        
        button_width = 15
        button_height = 3
        
        self.infinite_button = tk.Button(master, text="Oneindig", font=("Helvetica", 14), command=lambda: self.start_game("infinite"), bg="#4CAF50", fg="white", relief="raised", width=button_width, height=button_height)
        self.infinite_button.pack(pady=5)
        
        self.medium_button = tk.Button(master, text="Gemiddeld", font=("Helvetica", 14), command=lambda: self.start_game("medium"), bg="#4CAF50", fg="white", relief="raised", width=button_width, height=button_height)
        self.medium_button.pack(pady=5)
        
        self.hard_button = tk.Button(master, text="Moeilijk", font=("Helvetica", 14), command=lambda: self.start_game("hard"), bg="#4CAF50", fg="white", relief="raised", width=button_width, height=button_height)
        self.hard_button.pack(pady=5)

        self.settings_button = tk.Button(master, text="Instellingen", font=("Helvetica", 14), command=self.open_settings, bg="#4CAF50", fg="white", relief="raised", width=button_width, height=button_height)
        self.settings_button.pack(pady=5)

        self.close_button = tk.Button(master, text="Sluiten", font=("Helvetica", 14), command=self.confirm_exit, bg="#4CAF50", fg="white", relief="raised", width=button_width, height=button_height)
        self.close_button.pack(pady=5)

        # Initialize Pygame mixer for playing sound effects
        pygame.mixer.init()

        # Load button click sound effect
        self.button_click_sound = pygame.mixer.Sound("button_click.mp3")

        self.bind_button_click_sound()

        self.master.bind("<Escape>", lambda e: self.master.quit())

    def start_game(self, mode):
        # Read time setting from settings.txt
        try:
            with open("settings.txt", "r") as f:
                time_setting = f.read().strip()
        except FileNotFoundError:
            time_setting = "time30"  # Default time setting if file doesn't exist

        self.master.destroy()
        root = tk.Tk()
        game = NumberGuessingGame(root, mode, time_setting, self.button_click_sound)
        root.mainloop()

    def open_settings(self):
        self.master.destroy()
        root = tk.Tk()
        settings_page = SettingsPage(root)
        root.mainloop()

    def bind_button_click_sound(self):
        # Bind button click sound to all buttons
        buttons = [self.infinite_button, self.medium_button, self.hard_button, self.settings_button, self.close_button]
        for button in buttons:
            button.bind("<Button-1>", lambda event: self.play_button_click_sound())

    def play_button_click_sound(self):
        self.button_click_sound.play()

    def confirm_exit(self):
        confirmation = messagebox.askquestion("Afsluiten", "Wil je echt afsluiten?")
        if confirmation == "yes":
            sys.exit()


class SettingsPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Instellingen")
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg="#f0f0f0")
        
        self.title_label = tk.Label(master, text="Instellingen", font=("Helvetica", 20), bg="#f0f0f0")
        self.title_label.pack(pady=20)
        
        self.time_label = tk.Label(master, text="Tijdsinstellingen (seconden):", font=("Helvetica", 14), bg="#f0f0f0")
        self.time_label.pack()

        # Default, minimum, and maximum values for time settings
        self.default_time = 30
        self.min_time = 10
        self.max_time = 200

        # Read current time setting from settings.txt
        try:
            with open("settings.txt", "r") as f:
                current_time = f.read().strip()
                if current_time.startswith("time"):
                    current_time = current_time[4:]  # Remove "time" prefix
                    current_time = int(current_time)
                    if current_time < self.min_time or current_time > self.max_time:
                        current_time = self.default_time  # Reset to default if invalid value
                else:
                    current_time = self.default_time  # Default time setting if prefix is missing
        except FileNotFoundError:
            current_time = self.default_time  # Default time setting if file doesn't exist

        self.time_var = tk.StringVar(master, value=str(current_time))
        
        self.time_entry = tk.Entry(master, textvariable=self.time_var, font=("Helvetica", 14))
        self.time_entry.pack(pady=5)

        self.save_button = tk.Button(master, text="Opslaan", font=("Helvetica", 14), command=self.save_time_settings, bg="#4CAF50", fg="white", relief="raised")
        self.save_button.pack(pady=5)

        self.back_button = tk.Button(master, text="Terug", font=("Helvetica", 14), command=self.return_to_start_screen, bg="#4CAF50", fg="white", relief="raised")
        self.back_button.pack(pady=5)

        self.master.bind("<Escape>", lambda e: self.master.quit())

    def save_time_settings(self):
        try:
            time_value = int(self.time_var.get())
            if time_value < self.min_time or time_value > self.max_time:
                messagebox.showerror("Ongeldige Tijd", f"Tijd moet tussen {self.min_time} en {self.max_time} seconden zijn.")
                self.time_var.set(self.default_time)  # Reset to default
            else:
                # Save time settings to settings.txt
                with open("settings.txt", "w") as f:
                    f.write(f"time{time_value}")  # Prefix with "time"
                messagebox.showinfo("Succes", "Tijdsinstellingen opgeslagen.")
        except ValueError:
            messagebox.showerror("Fout", "Voer a.u.b. een geldig nummer in.")
            self.time_var.set(self.default_time)  # Reset to default

    def return_to_start_screen(self):
        self.master.destroy()
        root = tk.Tk()
        start_screen = StartScreen(root)
        root.mainloop()

def main():
    root = tk.Tk()
    start_screen = StartScreen(root)
    root.bind("<Escape>", lambda e: root.quit())  # Bind Escape key to close the game
    root.mainloop()

if __name__ == "__main__":
    main()

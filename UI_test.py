import tkinter as tk
from tkinter import PhotoImage

class ChessUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess UI")
        self.root.geometry("1024x600")  # Updated for 1024x600 touchscreen

        # Opening screen
        self.opening_screen = tk.Frame(root, bg="black")
        self.opening_screen.pack(fill="both", expand=True)

        # "Checkmate" label
        self.checkmate_label = tk.Label(
            self.opening_screen,
            text="Checkmate",
            font=("Arial", 36, "bold"),
            fg="white",
            bg="black"
        )
        self.checkmate_label.pack(pady=20)

        # Add logo
        self.logo = PhotoImage(file="logo.png")  # Replace with your logo path
        self.logo_label = tk.Label(self.opening_screen, image=self.logo, bg="black")
        self.logo_label.pack()

        # "Start" label
        self.start_label = tk.Label(
            self.opening_screen,
            text="Start",
            font=("Arial", 24),
            fg="white",
            bg="black"
        )
        self.start_label.pack(pady=20)

        # Bind any touch to the main menu
        self.opening_screen.bind("<Button-1>", self.show_main_menu)

        # Main menu screen
        self.main_menu = tk.Frame(root, bg="black")

        tk.Label(self.main_menu, text="Check-M.A.T.E", font=("Arial", 36), bg="white").pack(pady=20)
        
        self.custom_buttons = ["Play Online", "Play Bot", "Play Local", "Replay"]

        buttons = [
            {"label": self.custom_buttons[0], "command": self.start_game},
            {"label": self.custom_buttons[1], "command": self.custom_macros},
            {"label": self.custom_buttons[2], "command": self.open_settings},
            {"label": self.custom_buttons[3], "command": root.quit}
        ]

        for button in buttons:
            tk.Button(
                self.main_menu,
                text=button["label"],
                command=button["command"],
                font=("Arial", 18),
                width=20,
                bg="lightblue"
            ).pack(pady=10)

    def show_main_menu(self, event=None):
        """Switch to the main menu."""
        self.opening_screen.pack_forget()
        self.main_menu.pack(fill="both", expand=True)

    def start_game(self):
        print("Starting game...")

    def custom_macros(self):
        print("Opening custom macros...")

    def open_settings(self):
        print("Opening settings...")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessUI(root)
    root.mainloop()

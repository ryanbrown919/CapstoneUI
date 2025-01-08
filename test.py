import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Import Pillow for image resizing


class ChessUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Check-M.A.T.E")
        self.root.geometry("1024x600")  # Screen size
        self.root.configure(bg="black")  # Background color
        
        # Header
        header = tk.Frame(root, bg="black", height=100)
        header.pack(fill="x", side="top")
        
        title = tk.Label(
            header, text="Check-M.A.T.E", font=("Arial", 36, "bold"),
            fg="white", bg="black"
        )
        title.pack(side="left", padx=20)

        # Add resized logo
        original_logo = Image.open("Figures/logo.png")  # Replace with your logo path
        resized_logo = original_logo.resize((90, 121), Image.ANTIALIAS)  # Resize to 90x121 px
        self.logo = ImageTk.PhotoImage(resized_logo)        
        logo_label = tk.Label(header, image=self.logo, bg="black")
        logo_label.pack(side="right", padx=20)

        # Quickplay Section
        quickplay_frame = tk.Frame(root, bg="black")
        quickplay_frame.pack(fill="both", expand=True, pady=10)

        self.create_quickplay_button(quickplay_frame, "Play Online", "Figures/User.png", 0, 0)
        self.create_quickplay_button(quickplay_frame, "Play Bot", "🤖", 0, 1)
        self.create_quickplay_button(quickplay_frame, "Play Local", "👥", 0, 2)
        self.create_quickplay_button(quickplay_frame, "Replay", "🔄", 0, 3)

        # Footer Buttons
        footer = tk.Frame(root, bg="black")
        footer.pack(fill="x", side="bottom", pady=20)

        play_game_button = tk.Button(
            footer, text="▶ Play Game", font=("Arial", 20), bg="gray", fg="white",
            width=15, command=self.play_game
        )
        play_game_button.pack(side="left", padx=20)

        local_play_button = tk.Button(
            footer, text="Local Play\n10 min standard", font=("Arial", 18),
            bg="gray", fg="white", width=15, command=self.local_play
        )
        local_play_button.pack(side="right", padx=20)

    def create_quickplay_button(self, parent, text, icon, row, col):
        """Helper to create quickplay buttons."""
        button_frame = tk.Frame(parent, bg="darkgray", width=200, height=250)
        button_frame.grid(row=row, column=col, padx=20, pady=20)

        icon_label = tk.Label(button_frame, text=icon, font=("Arial", 24), bg="gray")
        icon_label.pack(pady=5)

        text_label = tk.Label(button_frame, text=text, font=("Arial", 16), bg="gray")
        text_label.pack()

    def play_game(self):
        print("Play Game button clicked.")

    def local_play(self):
        print("Local Play button clicked.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessUI(root)
    root.mainloop()

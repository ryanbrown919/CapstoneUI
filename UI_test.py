import tkinter as tk
from tkinter import simpledialog
from time import sleep

class ChessUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess UI")
        
        # Main menu
        self.main_menu = tk.Frame(root)
        tk.Label(self.main_menu, text="Chess Menu", font=("Arial", 24)).pack(pady=10)
        tk.Button(self.main_menu, text="Start Game", command=self.start_game).pack(pady=5)
        tk.Button(self.main_menu, text="Custom Macros", command=self.show_macros).pack(pady=5)
        tk.Button(self.main_menu, text="Exit", command=root.quit).pack(pady=5)
        self.main_menu.pack()
        
        # Chess Clock UI
        self.clock_frame = tk.Frame(root)
        self.time_left = {"Player 1": 300, "Player 2": 300}  # Default 5 minutes each
        self.active_player = "Player 1"
        self.clock_labels = {
            "Player 1": tk.Label(self.clock_frame, text="Player 1: 05:00", font=("Arial", 18)),
            "Player 2": tk.Label(self.clock_frame, text="Player 2: 05:00", font=("Arial", 18))
        }
        for player, label in self.clock_labels.items():
            label.pack()
        tk.Button(self.clock_frame, text="Switch Player", command=self.switch_player).pack(pady=5)
        tk.Button(self.clock_frame, text="Back to Menu", command=self.show_menu).pack(pady=5)
        self.running = False

    def start_game(self):
        self.running = True
        self.main_menu.pack_forget()
        self.clock_frame.pack()
        self.update_clock()

    def switch_player(self):
        self.active_player = "Player 2" if self.active_player == "Player 1" else "Player 1"

    def update_clock(self):
        if self.running:
            self.time_left[self.active_player] -= 1
            for player, time in self.time_left.items():
                mins, secs = divmod(time, 60)
                self.clock_labels[player].config(text=f"{player}: {mins:02}:{secs:02}")
            if self.time_left[self.active_player] > 0:
                self.root.after(1000, self.update_clock)
            else:
                self.running = False
                tk.Label(self.clock_frame, text=f"{self.active_player} ran out of time!", font=("Arial", 18)).pack()

    def show_macros(self):
        macros = simpledialog.askstring("Custom Macros", "Enter macro details (e.g., Open Sicilian):")
        if macros:
            tk.Label(self.main_menu, text=f"Macro Added: {macros}").pack()

    def show_menu(self):
        self.running = False
        self.clock_frame.pack_forget()
        self.main_menu.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x480")  # Adjust for your 7-inch touchscreen
    app = ChessUI(root)
    root.mainloop()

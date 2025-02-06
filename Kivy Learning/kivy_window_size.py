import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp, sp

# Force Kivy to use a density of 1

# Set the window size
Window.size = (dp(1024), dp(600))
Window.top = 0
Window.left = 0
Window.dpi = 96

print(f"Window size: {Window.size}")
print(f"Window DPI: {Window.dpi}")


class ChessPiece(ButtonBehavior, Image):
    """A chess piece that can be clicked."""
    def __init__(self, square_size, board_offset, **kwargs):
        super().__init__(**kwargs)
        self.square_size = square_size
        self.board_offset = board_offset
        self.selected = False
        

    def select(self):
        """Mark the piece as selected."""
        self.selected = True
        self.color = (0.5, 0.5, 1, 1)  # Highlight with blue tint

    def deselect(self):
        """Deselect the piece."""
        self.selected = False
        self.color = (1, 1, 1, 1)  # Restore original color


class ChessBoard(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board_size = 480  # Chessboard size
        self.square_size = self.board_size // 8  # Size of each square
        self.selected_piece = None  # Currently selected piece
        self.occupied_squares = set()  # Keep track of occupied squares
        self.build_board()
        self.add_pawn()

    def build_board(self):
        """Draw the chessboard grid."""
        self.canvas.clear()
        colors = [(1, 1, 1, 1), (0.5, 0.5, 0.5, 1)]  # Alternating colors (white and gray)

        # Center the chessboard within the Kivy window
        self.center_x = (Window.width - self.board_size) / 2
        self.center_y = (Window.height - self.board_size) / 2

        with self.canvas:
            for row in range(8):
                for col in range(8):
                    color_index = (row + col) % 2
                    Color(*colors[color_index])
                    Rectangle(
                        pos=(self.center_x + col * self.square_size,
                             self.center_y + row * self.square_size),
                        size=(self.square_size, self.square_size)
                    )

    def add_pawn(self):
        """Add a clickable pawn to the chessboard."""
        # Start at e2 (4th column, 1st row from bottom)
        col = 4
        row = 1
        initial_pos = self.get_square_center(col, row)
        self.occupied_squares.add((col, row))  # Mark the square as occupied

        pawn = ChessPiece(
            square_size=self.square_size,
            board_offset=(self.center_x, self.center_y),
            source="figures/white_pawn.png",  # Replace with your pawn image path
            size_hint=(None, None),
            size=(self.square_size, self.square_size),
            pos=(initial_pos[0] - self.square_size / 2, initial_pos[1] - self.square_size / 2)
        )
        pawn.bind(on_press=self.select_piece)
        self.add_widget(pawn)

    def select_piece(self, instance):
        """Handle piece selection."""
        if self.selected_piece == instance:
            # Deselect if clicking the already selected piece
            self.selected_piece.deselect()
            self.selected_piece = None
        else:
            # Select a new piece
            if self.selected_piece:
                self.selected_piece.deselect()
            self.selected_piece = instance
            self.selected_piece.select()

    def on_touch_down(self, touch):
        """Handle movement of the selected piece."""
        if self.selected_piece and self.collide_point(*touch.pos):
            # Calculate the nearest square
            col = round((touch.x - self.center_x) / self.square_size)
            row = round((touch.y - self.center_y) / self.square_size)

            # Check if the square is empty
            if (col, row) not in self.occupied_squares:
                # Update piece position
                new_pos = self.get_square_center(col, row)

                # Safely handle old position
                old_col, old_row = self.get_square_indices(self.selected_piece.pos)
                if (old_col, old_row) in self.occupied_squares:
                    self.occupied_squares.remove((old_col, old_row))

                self.selected_piece.pos = (
                    new_pos[0] - self.square_size / 2, 
                    new_pos[1] - self.square_size / 2
                )

                # Update occupied squares
                self.occupied_squares.add((col, row))

                self.selected_piece.deselect()
                self.selected_piece = None
        return super().on_touch_down(touch)

    def get_square_center(self, col, row):
        """Get the center position of a square based on its column and row."""
        x = self.center_x + col * self.square_size + self.square_size / 2
        y = self.center_y + row * self.square_size + self.square_size / 2
        return x, y

    def get_square_indices(self, pos):
        """Get the column and row indices for a given position."""
        col = round((pos[0] - self.center_x) / self.square_size)
        row = round((pos[1] - self.center_y) / self.square_size)
        return col, row


class ChessApp(App):
    def build(self):
        return ChessBoard()


if __name__ == "__main__":
    ChessApp().run()

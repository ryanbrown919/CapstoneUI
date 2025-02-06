from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

# Set window size for clarity
Window.size = (960, 540)
Window.left = 0
Window.top = 0

class SelectablePiece(Image):
    def __init__(self, square_size, board_offset, **kwargs):
        super().__init__(**kwargs)
        self.square_size = square_size
        self.board_offset = board_offset  # Offset of the board within the Kivy window
        self.selected = False
        self.default_color = (1, 1, 1, 1)  # Default color
        self.selected_color = (0.5, 0.5, 1, 1)  # Highlight selected piece

    def select(self):
        self.selected = True
        self.color = self.selected_color  # Highlight selected piece

    def deselect(self):
        self.selected = False
        self.color = self.default_color  # Restore original color
    def __init__(self, square_size, board_offset, **kwargs):
        super().__init__(**kwargs)
        self.square_size = square_size
        self.board_offset = board_offset  # Offset of the board within the Kivy window
        self.selected = False

    def select(self):
        self.selected = True
        self.color = (0.5, 0.5, 1, 1)  # Highlight selected piece

    def deselect(self):
        self.selected = False
        self.color = (1, 1, 1, 1)  # Restore original color


class ChessBoard(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board_size = 960  # Chessboard size
        self.square_size = self.board_size // 8  # Size of each square
        self.selected_piece = None
        self.highlighted_squares = []
        self.build_board()
        self.add_pieces()

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
                        pos=(self.center_x + col * self.square_size,  # Offset by board position
                             self.center_y + row * self.square_size),
                        size=(self.square_size, self.square_size)
                    )

    def add_pieces(self):
        """Add all chess pieces to their initial positions."""
        piece_positions = {
            'white_rook': [(7, 0), (7, 7)],
            'white_knight': [(7, 1), (7, 6)],
            'white_bishop': [(7, 2), (7, 5)],
            'white_queen': [(7, 3)],
            'white_king': [(7, 4)],
            'white_pawn': [(6, col) for col in range(8)],

            'black_rook': [(0, 0), (0, 7)],
            'black_knight': [(0, 1), (0, 6)],
            'black_bishop': [(0, 2), (0, 5)],
            'black_queen': [(0, 3)],
            'black_king': [(0, 4)],
            'black_pawn': [(1, col) for col in range(8)],
        }

        piece_images = {
            'white_rook': 'figures/white_rook.png',
            'white_knight': 'figures/white_knight.png',
            'white_bishop': 'figures/white_bishop.png',
            'white_queen': 'figures/white_queen.png',
            'white_king': 'figures/white_king.png',
            'white_pawn': 'figures/white_pawn.png',
            'black_rook': 'figures/black_rook.png',
            'black_knight': 'figures/black_knight.png',
            'black_bishop': 'figures/black_bishop.png',
            'black_queen': 'figures/black_queen.png',
            'black_king': 'figures/black_king.png',
            'black_pawn': 'figures/black_pawn.png',
        }

        for piece, positions in piece_positions.items():
            for row, col in positions:
                piece_image = SelectablePiece(
                    square_size=self.square_size,
                    board_offset=(self.center_x, self.center_y),
                    source=piece_images[piece],  # Load the appropriate image
                    size_hint=(None, None),
                    size=(self.square_size, self.square_size),
                    pos=(self.center_x + col * self.square_size,
                         self.center_y + row * self.square_size)
                )
                piece_image.bind(on_touch_down=self.select_piece)
                self.add_widget(piece_image)

    def select_piece(self, instance, touch):
        """Handle selecting and deselecting a piece, and highlight possible moves."""
        print(touch.x, touch.y)
        if instance.collide_point(touch.x, touch.y):
            print(True)
            if self.selected_piece == instance:
                # Deselect the piece if it's already selected
                self.clear_highlights()
                self.selected_piece.deselect()
                self.selected_piece = None
            else:
                # Select the new piece
                if self.selected_piece:
                    self.clear_highlights()
                    self.selected_piece.deselect()

                self.selected_piece = instance
                self.selected_piece.select()
                self.highlight_moves(self.selected_piece)
        else:
            if self.selected_piece:
                self.clear_highlights()
                self.selected_piece.deselect()
                self.selected_piece = None

    def highlight_moves(self, piece):
        """Highlight possible moves for the selected piece."""
        self.clear_highlights()

        # Example: Highlight all squares in the same column for pawns
        for i in range(8):
            x = piece.board_offset[0] + i * piece.square_size
            y = piece.y  # Highlight along the current row for simplicity

            with self.canvas:
                Color(0.5, 1, 0.5, 0.5)  # Green with transparency
                rect = Rectangle(
                    pos=(x, piece.board_offset[1] + (i * piece.square_size)),
                    size=(self.square_size, self.square_size)
                )
                self.highlighted_squares.append(rect)

    def clear_highlights(self):
        """Clear all highlighted squares."""
        for rect in self.highlighted_squares:
            self.canvas.remove(rect)
        self.highlighted_squares = []

    def on_touch_down(self, touch):
        """Handle moving the selected piece."""
        if self.selected_piece:
            # Calculate the column and row based on the touch position relative to the bottom-left of the white side of the board
            col = max(0, min(7, int((touch.x - self.center_x) // self.square_size)))
            row = max(0, min(7, int((touch.y - self.center_y) // self.square_size)))

            # Print the calculated row and column for debugging
            print(f"Clicked square: column={col}, row={row}")

            # Check if a valid square is clicked
            if 0 <= col < 8 and 0 <= row < 8:
                self.selected_piece.pos = (
                    self.center_x + col * self.square_size,
                    self.center_y + row * self.square_size
                )

                self.clear_highlights()
                self.selected_piece.deselect()
                self.selected_piece = None
        else:
            super().on_touch_down(touch)
        """Handle moving the selected piece."""
        if self.selected_piece:
            # Calculate the column and row based on the touch position relative to the bottom-left of the board
            col = int((touch.x - self.center_x) // self.square_size)
            row = int((touch.y - self.center_y) // self.square_size)

            # Print the calculated row and column for debugging
            print(f"Clicked square: column={col}, row={row}")

            # Check if a valid square is clicked
            if 0 <= col < 8 and 0 <= row < 8:
                self.selected_piece.pos = (
                    self.center_x + col * self.square_size,
                    self.center_y + row * self.square_size
                )

                self.clear_highlights()
                self.selected_piece.deselect()
                self.selected_piece = None
        else:
            super().on_touch_down(touch)
        """Handle moving the selected piece."""
        if self.selected_piece:
            # Check if a valid square is clicked
            col = round((touch.x - self.center_x) / self.square_size)
            row = round((touch.y - self.center_y) / self.square_size)

            print(f"Clicked square: column={col}, row={row}")

            if 0 <= col < 8 and 0 <= row < 8:
                self.selected_piece.pos = (
                    self.center_x + col * self.square_size,
                    self.center_y + row * self.square_size
                )

                self.clear_highlights()
                self.selected_piece.deselect()
                self.selected_piece = None
        else:
            super().on_touch_down(touch)


class ChessApp(App):
    def build(self):
        return ChessBoard()


if __name__ == "__main__":
    ChessApp().run()

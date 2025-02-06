from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.behaviors import DragBehavior
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

# Set window size for clarity
Window.size = (1920, 1080)
Window.left = 0
Window.top = 0

class DraggablePiece(DragBehavior, Image):
    def __init__(self, square_size, board_offset, **kwargs):
        super().__init__(**kwargs)
        self.square_size = square_size
        self.board_offset = board_offset  # Offset of the board within the Kivy window
        self.drag_timeout = 10000000
        self.drag_distance = 0

    def on_touch_move(self, touch):
        """Show the piece moving dynamically with the pointer."""
        if self.collide_point(*touch.pos):
            self.pos = (touch.x - self.width / 2, touch.y - self.height / 2)
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        """Snap the piece to the nearest square after release."""
        if self.collide_point(*touch.pos):
            # Calculate the nearest square
            col = round((self.x - self.board_offset[0]) / self.square_size)
            row = round((self.y - self.board_offset[1]) / self.square_size)
            snapped_x = self.board_offset[0] + col * self.square_size
            snapped_y = self.board_offset[1] + row * self.square_size
            self.pos = (snapped_x, snapped_y)  # Snap to the center of the nearest square
        return super().on_touch_up(touch)


class ChessBoard(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board_size = 960  # Chessboard size
        self.square_size = self.board_size // 8  # Size of each square
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
                piece_image = DraggablePiece(
                    square_size=self.square_size,
                    board_offset=(self.center_x, self.center_y),
                    source=piece_images[piece],  # Load the appropriate image
                    size_hint=(None, None),
                    size=(self.square_size, self.square_size),
                    pos=(self.center_x + col * self.square_size,
                         self.center_y + row * self.square_size)
                )
                self.add_widget(piece_image)


class ChessApp(App):
    def build(self):
        return ChessBoard()


if __name__ == "__main__":
    ChessApp().run()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import DragBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


# Draggable chess piece
class DraggableImage(DragBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drag_timeout = 10000000
        self.drag_distance = 0


# Chessboard screen
class ChessBoardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_board()

    def create_board(self):
        # Create a grid layout for the chessboard
        board_layout = GridLayout(cols=8, size_hint=(1, 1))
        colors = [(1, 1, 1, 1), (0.5, 0.5, 0.5, 1)]  # White and gray squares

        # Add squares to the board
        for row in range(8):
            for col in range(8):
                color_index = (row + col) % 2
                square = Widget()
                with square.canvas.before:
                    Color(*colors[color_index])
                    Rectangle(pos=square.pos, size=(100, 100))
                board_layout.add_widget(square)

        # Add pieces to their initial positions
        self.add_pieces(board_layout)

        # Add the chessboard to the screen
        self.add_widget(board_layout)

    def add_pieces(self, board_layout):
        # Initial positions of pieces
        piece_positions = {
            'rook': [(0, 0), (0, 7), (7, 0), (7, 7)],
            'knight': [(0, 1), (0, 6), (7, 1), (7, 6)],
            'bishop': [(0, 2), (0, 5), (7, 2), (7, 5)],
            'queen': [(0, 3), (7, 3)],
            'king': [(0, 4), (7, 4)],
            'pawn': [(1, col) for col in range(8)] + [(6, col) for col in range(8)],
        }

        # Map piece names to image files
        piece_images = {
            'rook': 'rook.png',
            'knight': 'knight.png',
            'bishop': 'bishop.png',
            'queen': 'queen.png',
            'king': 'king.png',
            'pawn': 'pawn.png',
        }

        for piece, positions in piece_positions.items():
            for row, col in positions:
                piece_image = DraggableImage(
                    source=piece_images[piece],
                    size_hint=(None, None),
                    size=(100, 100)
                )
                # Add piece to the correct grid cell
                board_layout.add_widget(piece_image, row * 8 + col)


# Main application
class ChessApp(App):
    def build(self):
        # Screen manager to handle multiple screens
        sm = ScreenManager()
        sm.add_widget(ChessBoardScreen(name='chess_board'))
        return sm


if __name__ == '__main__':
    ChessApp().run()

from kivy.config import Config

# Set the window size BEFORE importing other Kivy modules
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'multisamples', '0')  # Disable anti-aliasing
Config.set('graphics', 'allow_screensaver', False)
Config.set('graphics', 'fullscreen', '0')  # Ensure windowed mode
Config.set('kivy', 'exit_on_escape', '1')  # Allow exiting with ESC

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.behaviors import DragBehavior
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

# Get screen dimensions using tkinter (cross-platform)
screen_width = 2560
screen_height = 1600

# Set Kivy window size
Window.size = (1024, 600)

# Center the Kivy window on the screen
#Window.left = (screen_width - Window.width) // 2
#Window.top = (screen_height - Window.height) // 2
Window.left = 0
Window.top = 0


# class DraggablePawn(DragBehavior, Image):
#     def __init__(self, square_size, board_offset, **kwargs):
#         super().__init__(**kwargs)
#         self.square_size = square_size
#         self.board_offset = board_offset  # Offset of the board within the Kivy window
#         self.drag_timeout = 10000000
#         self.drag_distance = 0

#     def on_touch_move(self, touch):
#         # Snap to the nearest square on release
#         if self.collide_point(*touch.pos):
#             col = round((self.x - self.board_offset[0]) / self.square_size)
#             row = round((self.y - self.board_offset[1]) / self.square_size)
#             snapped_x = self.board_offset[0] + col * self.square_size
#             snapped_y = self.board_offset[1] + row * self.square_size
#             #self.pos = (snapped_x, snapped_y)
#             print(snapped_x, snapped_y)
#             self.pos = touch.pos[0] - self.width / 2, touch.pos[1] - self.height / 2

#         return super().on_touch_move(touch)

class DraggablePawn(DragBehavior, Image):
    def __init__(self, square_size, board_offset, **kwargs):
        super().__init__(**kwargs)
        self.square_size = square_size
        self.board_offset = board_offset  # Offset of the board within the Kivy window
        self.drag_timeout = 10000000
        self.drag_distance = 0

    def on_touch_move(self, touch):
        """Show the pawn moving dynamically with the pointer."""
        if self.collide_point(*touch.pos):
            self.pos = (touch.x - self.width / 2, touch.y - self.height / 2)
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        """Snap the pawn to the nearest square after release."""
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
        self.board_size = 592  # Chessboard size
        self.square_size = self.board_size // 8  # Size of each square
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
                        pos=(self.center_x + col * self.square_size,  # Offset by board position
                             self.center_y + row * self.square_size),
                        size=(self.square_size, self.square_size)
                    )

    def add_pawn(self):
        """Add a draggable pawn to the chessboard."""
        pawn = DraggablePawn(
            square_size=self.square_size,
            board_offset=(self.center_x, self.center_y),
            source="figures/white_pawn.png",  # Replace with the path to your pawn image
            size_hint=(None, None),
            size=(self.square_size, self.square_size),
            pos=(self.center_x + 4 * self.square_size,  # Start at e2 (4th column, 1st row)
                 self.center_y + 1 * self.square_size)
        )
        self.add_widget(pawn)


class ChessApp(App):
    def build(self):
        return ChessBoard()


if __name__ == "__main__":
    ChessApp().run()

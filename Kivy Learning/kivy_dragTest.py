from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.graphics import Color, Rectangle


class DraggableRectangle(DragBehavior, Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (100, 100)  # Dimensions of the rectangle
        self.pos = (200, 200)  # Initial position of the rectangle

        # Draw the rectangle
        with self.canvas:
            Color(0, 1, 0, 1)  # Green color
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def on_touch_move(self, touch):
        # Update the rectangle's position when dragged
        if self.collide_point(*touch.pos):
            self.pos = touch.pos[0] - self.width / 2, touch.pos[1] - self.height / 2
            self.rect.pos = self.pos  # Update the graphics
        return super().on_touch_move(touch)


class DragApp(App):
    def build(self):
        root = Widget()
        rect = DraggableRectangle()
        root.add_widget(rect)
        return root


if __name__ == "__main__":
    DragApp().run()

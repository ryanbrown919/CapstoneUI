from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Define screens using Kivy Language
kv = """
ScreenManager:
    HomeScreen:
    GameScreen:

<HomeScreen>:
    name: 'home'
    BoxLayout:
        orientation: 'vertical'
        spacing: 20
        padding: 50

        Label:
            text: 'Welcome to Checkmate!'
            font_size: '32sp'
            size_hint_y: 0.2

        Button:
            text: 'Start Game'
            font_size: '24sp'
            size_hint: (0.6, 0.2)
            pos_hint: {'center_x': 0.5}
            on_press: root.manager.current = 'game'

        Button:
            text: 'Settings'
            font_size: '24sp'
            size_hint: (0.6, 0.2)
            pos_hint: {'center_x': 0.5}
            on_press: app.open_settings()

<GameScreen>:
    name: 'game'
    BoxLayout:
        orientation: 'vertical'
        spacing: 20
        padding: 50

        Label:
            text: 'Game Screen'
            font_size: '32sp'
            size_hint_y: 0.2

        Button:
            text: 'Back to Home'
            font_size: '24sp'
            size_hint: (0.6, 0.2)
            pos_hint: {'center_x': 0.5}
            on_press: root.manager.current = 'home'
"""

class HomeScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class ChessApp(App):
    def build(self):
        return Builder.load_string(kv)

if __name__ == '__main__':
    ChessApp().run()

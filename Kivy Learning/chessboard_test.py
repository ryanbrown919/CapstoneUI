from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

# Kivy Layout for UI
kv = """
ScreenManager:
    MainMenuScreen:
    ChessBoardScreen:

<MainMenuScreen>:
    name: 'main_menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        # Header
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1
            Label:
                text: 'Check-M.A.T.E'
                font_size: '32sp'
                halign: 'left'
            Image:
                source: 'chess_icon.png'  # Replace with your icon image
                size_hint_x: 0.2

        # Quickplay Buttons
        Label:
            text: 'Quickplay'
            font_size: '20sp'
            size_hint_y: 0.1

        GridLayout:
            cols: 4
            spacing: 10
            size_hint_y: 0.4

            Button:
                text: 'Play Online\\n10 min standard'
                font_size: '16sp'
                background_normal: ''
                background_color: (0.5, 0.5, 0.5, 1)
                on_press: app.play_online()

            Button:
                text: 'Play Bot\\n10 min standard'
                font_size: '16sp'
                background_normal: ''
                background_color: (0.5, 0.5, 0.5, 1)
                on_press: app.play_bot()

            Button:
                text: 'Play Local\\n10 min standard'
                font_size: '16sp'
                background_normal: ''
                background_color: (0.5, 0.5, 0.5, 1)
                on_press: app.play_local()

            Button:
                text: 'Replay\\n10 min standard'
                font_size: '16sp'
                background_normal: ''
                background_color: (0.5, 0.5, 0.5, 1)
                on_press: app.replay_game()

        # Main Buttons
        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            size_hint_y: 0.2

            Button:
                text: 'Play Game'
                font_size: '24sp'
                on_press: root.manager.current = 'chess_board'

            Button:
                text: 'Local Play\\n10 min standard'
                font_size: '16sp'
                background_normal: ''
                background_color: (0.5, 0.5, 0.5, 1)

        # Footer Buttons
        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            size_hint_y: 0.1

            Button:
                text: 'Home'
                font_size: '16sp'
                on_press: app.go_home()

            Button:
                text: 'Settings'
                font_size: '16sp'
                on_press: app.open_settings()

            Button:
                text: 'Power Off'
                font_size: '16sp'
                on_press: app.power_off()

<ChessBoardScreen>:
    name: 'chess_board'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Chess Board Placeholder'
            font_size: '32sp'
        Button:
            text: 'Back to Main Menu'
            font_size: '20sp'
            on_press: root.manager.current = 'main_menu'
"""

# Python App Logic
class MainMenuScreen(Screen):
    pass

class ChessBoardScreen(Screen):
    pass

class ChessApp(App):
    def build(self):
        return Builder.load_string(kv)

    def play_online(self):
        print("Play Online pressed!")

    def play_bot(self):
        print("Play Bot pressed!")

    def play_local(self):
        print("Play Local pressed!")

    def replay_game(self):
        print("Replay Game pressed!")

    def go_home(self):
        print("Home pressed!")

    def open_settings(self):
        print("Settings pressed!")

    def power_off(self):
        print("Power Off pressed!")

if __name__ == '__main__':
    ChessApp().run()

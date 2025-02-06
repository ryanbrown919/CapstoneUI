# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from feb2_working import ChessGameWidget
from feb6_chessclock import ChessClockWidget
from feb6_gantrycontrol import GantryControlWidget

# Optionally, import your custom Kivy UI code here:
# from my_chess_ui import MyChessWidget

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Button to go to chess playing mode (chessboard screen)
        btn_chess = Button(text="Chess Playing Mode", size_hint=(1, 0.3))
        btn_chess.bind(on_release=lambda instance: self.change_screen("chess"))
        layout.add_widget(btn_chess)

        # Button to go to manual gantry control screen
        btn_gantry = Button(text="Manual Gantry Control", size_hint=(1, 0.3))
        btn_gantry.bind(on_release=lambda instance: self.change_screen("gantry"))
        layout.add_widget(btn_gantry)

        # Button to go to chess clock tester screen
        btn_clock = Button(text="Chess Clock Tester", size_hint=(1, 0.3))
        btn_clock.bind(on_release=lambda instance: self.change_screen("clock"))
        layout.add_widget(btn_clock)

        self.add_widget(layout)

    def change_screen(self, screen_name):
        # Set the transition direction for moving forward
        self.manager.transition.direction = 'left'
        self.manager.current = screen_name

class BaseScreen(Screen):
    """
    Base screen with a reusable back button placed at the top left.
    """
    def add_back_button(self, parent_layout):
        # Create a small back button and position it at the top left
        back_btn = Button(text="Back", size_hint=(None, None), size=(100, 50),
                          pos_hint={'x': 0, 'y': 0})
        back_btn.bind(on_release=lambda instance: self.go_back())
        parent_layout.add_widget(back_btn)

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "menu"

class ChessGameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(ChessGameScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Insert your Kivy UI code here.
        # For instance, if you have a custom widget, use:
        chess_board = ChessGameWidget()
        layout.add_widget(chess_board)
        #layout.add_widget(Label(text="Chess Playing Mode\n(Chessboard UI goes here)", font_size=24))

        # Add the back button with reverse animation
        self.add_back_button(layout)
        self.add_widget(layout)

class GantryControlScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(GantryControlScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        gantry_control = GantryControlWidget()
        layout.add_widget(gantry_control)

        # Insert your manual gantry control UI code here.
        #layout.add_widget(Label(text="Manual Gantry Control", font_size=24))

        # Add the back button
        self.add_back_button(layout)
        self.add_widget(layout)

class ChessClockTesterScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(ChessClockTesterScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)


        chess_clock = ChessClockWidget()
        layout.add_widget(chess_clock)
        # Insert your chess clock tester UI code here.
        #layout.add_widget(Label(text="Chess Clock Tester", font_size=24))

        # Add the back button
        self.add_back_button(layout)
        self.add_widget(layout)

class FullApp(App):
    def build(self):
        # Optionally, you can specify the type of transition here:
        sm = ScreenManager(transition=SlideTransition())
        # Create and add the main menu and additional screens.
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(ChessGameScreen(name="chess"))
        sm.add_widget(GantryControlScreen(name="gantry"))
        sm.add_widget(ChessClockTesterScreen(name="clock"))
        return sm

if __name__ == '__main__':
    FullApp().run()

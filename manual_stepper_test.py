from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
import serial

# Establish serial connection to Arduino
arduino = serial.Serial('/dev/cu.usbserial-10', 9600, timeout=1)  # Replace 'COM3' with your Arduino port

class GantryControlApp(App):
    def build(self):
        self.speed = 0
        self.main_layout = BoxLayout(orientation='vertical')

        # Slider for speed control
        self.speed_label = Label(text=f"Speed: {self.speed}")
        self.main_layout.add_widget(self.speed_label)

        self.speed_slider = Slider(min=0, max=255, value=self.speed)
        self.speed_slider.bind(value=self.on_speed_change)
        self.main_layout.add_widget(self.speed_slider)

        # WASD controls for gantry motion
        controls_label = Label(text="Use WASD keys for motion")
        self.main_layout.add_widget(controls_label)
        
        # Event bindings for key input
        Window.bind(on_key_down=self.on_key_down)

        return self.main_layout

    def on_speed_change(self, instance, value):
        self.speed = int(value)
        self.speed_label.text = f"Speed: {self.speed}"
        self.send_command(f"speed:{self.speed}")

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        command = None
        if text.lower() == 'w':
            command = "motion:up"
        elif text.lower() == 's':
            command = "motion:down"
        elif text.lower() == 'a':
            command = "motion:left"
        elif text.lower() == 'd':
            command = "motion:right"

        if command:
            self.send_command(command)

    def send_command(self, command):
        if arduino.is_open:
            arduino.write(f"{command}\n".encode('utf-8'))

    def on_stop(self):
        if arduino.is_open:
            arduino.close()

if __name__ == '__main__':
    GantryControlApp().run()

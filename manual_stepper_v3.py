from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
import serial
import time

# Establish serial connection to Arduino
#arduino = serial.Serial('/dev/cu.usbserial-10', 9600, timeout=1)  # Replace with your port


class GantryControlApp(App):
    def build(self):
        self.speed = 0
        self.keys_pressed = set()  # Track currently pressed keys
        self.last_command_time = time.time()  # Timestamp of the last command sent
        self.cooldown_period = 0.2  # Cooldown period in seconds
        self.main_layout = BoxLayout(orientation='vertical')

        # Slider for speed control
        self.speed_label = Label(text=f"Speed: {self.speed}")
        self.main_layout.add_widget(self.speed_label)

        self.speed_slider = Slider(min=0, max=2000, value=self.speed)
        self.speed_slider.bind(value=self.on_speed_change)
        self.main_layout.add_widget(self.speed_slider)

        # Instructions for WASD controls
        controls_label = Label(text="Use WASD keys for motion")
        self.main_layout.add_widget(controls_label)

        # Bind key events
        Window.bind(on_key_down=self.on_key_down)

        # Schedule periodic key state checking
        Clock.schedule_interval(self.update_motion, 0.1)

        return self.main_layout

    def on_speed_change(self, instance, value):
        self.speed = int(value)
        self.speed_label.text = f"Speed: {self.speed}"
        self.send_command(f"speed:{self.speed}")

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if text.lower() in ['w', 'a', 's', 'd']:
            self.keys_pressed.add(text.lower())  # Add the key to the set of pressed keys

    def update_motion(self, dt):
        # Check if we are within the cooldown period
        current_time = time.time()
        if current_time - self.last_command_time < self.cooldown_period:
            return  # Still in cooldown, continue moving

        # Determine the motion command based on the currently pressed keys
        command = "motion:stop"  # Default command
        if 'w' in self.keys_pressed:
            command = "motion:up"
        elif 's' in self.keys_pressed:
            command = "motion:down"
        elif 'a' in self.keys_pressed:
            command = "motion:left"
        elif 'd' in self.keys_pressed:
            command = "motion:right"

        # Send the motion command and update the last command time
        self.send_command(command)
        self.last_command_time = current_time

        # Clear the keys_pressed set to ensure key release is handled properly
        self.keys_pressed.clear()

    def send_command(self, command):
        if arduino.is_open:
            arduino.write(f"{command}\n".encode('utf-8'))
        return

    def on_stop(self):
        if arduino.is_open:
            arduino.close()
        return


if __name__ == '__main__':
    GantryControlApp().run()

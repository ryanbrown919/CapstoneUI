from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.clock import Clock
import threading
import time
import sys
from kivy.app import App

# Check platform for compatibility
running_on_pi = sys.platform.startswith("linux")

if running_on_pi:
    import board
    import busio
    from adafruit_pn532.i2c import PN532_I2C

# Mock NFC Code-to-Icon Mapping
NFC_TAG_MAP = {
    "123456789": "figures/white_pawn.png",
    "987654321": "knight.png",
    "111222333": "bishop.png",
    "444555666": "rook.png",
    "777888999": "queen.png",
    "000111222": "king.png",
}

class NFCReaderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.layout = GridLayout(cols=2)
        
        # Left side layout for the log
        log_layout = BoxLayout(orientation='vertical', size_hint=(0.4, 1))
        self.log_label = Label(text="Scan Log:\n", size_hint=(1, 1), halign="left", valign="top")
        self.log_label.bind(size=self.log_label.setter('text_size'))
        scroll_view = ScrollView()
        scroll_view.add_widget(self.log_label)
        log_layout.add_widget(scroll_view)
        self.layout.add_widget(log_layout)
        
        # Right side layout
        right_layout = BoxLayout(orientation='vertical', size_hint=(0.6, 1))
        
        # Icon display in the top-right
        self.icon_display = Image(source="pawn.png", size_hint=(1, 0.5))  # Default to pawn
        right_layout.add_widget(self.icon_display)
        
        # Buttons in the bottom-left
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.read_button = Button(text="Read NFC", size_hint=(0.5, 1))
        self.read_button.bind(on_press=self.read_nfc)
        button_layout.add_widget(self.read_button)
        
        self.reconnect_button = Button(text="Reconnect", size_hint=(0.5, 1))
        self.reconnect_button.bind(on_press=self.connect_reader)
        button_layout.add_widget(self.reconnect_button)
        
        right_layout.add_widget(button_layout)
        self.layout.add_widget(right_layout)
        
        self.add_widget(self.layout)
        
        if running_on_pi:
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.pn532 = None
            self.connect_reader()
        else:
            self.pn532 = None
            self.log("Running on non-Pi system. NFC scanning is simulated.")

    def connect_reader(self, instance=None):
        if running_on_pi:
            try:
                self.pn532 = PN532_I2C(self.i2c, debug=False)
                self.pn532.SAM_configuration()
                self.log("PN532 Reader connected successfully.")
            except Exception as e:
                self.log(f"Failed to connect: {e}")
                self.pn532 = None
        else:
            self.log("NFC Reader unavailable on this system.")

    def read_nfc(self, instance):
        if self.pn532:
            threading.Thread(target=self.scan_nfc, daemon=True).start()
        else:
            self.log("No NFC reader detected. Simulating a pawn scan.")
            self.update_display("123456789")
    
    def scan_nfc(self):
        if self.pn532:
            self.log("Waiting for an NFC tag...")
            uid = self.pn532.read_passive_target(timeout=0.5)
            if uid:
                tag_id = ''.join(map(str, uid))
                self.log(f"Tag scanned: {tag_id}")
                self.update_display(tag_id)
            else:
                self.log("No tag found.")

    def update_display(self, tag_id):
        icon_source = NFC_TAG_MAP.get(tag_id, "pawn.png")  # Default to pawn if unknown
        self.icon_display.source = icon_source
        self.icon_display.reload()
        self.log(f"Updated display to {icon_source}")

    def log(self, message):
        self.log_label.text += f"\n{message}"

class NFCApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(NFCReaderScreen(name='nfc_reader'))
        return sm

if __name__ == "__main__":
    NFCApp().run()
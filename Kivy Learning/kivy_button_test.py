from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.label = Label(text="Click a button!", font_size='24sp')
        layout.add_widget(self.label)

        self.dynamic_button = Button(text="Dynamic Button", font_size='20sp')
        self.dynamic_button.bind(on_press=self.default_action)
        layout.add_widget(self.dynamic_button)

        change_button = Button(text="Change Action", font_size='20sp')
        change_button.bind(on_press=self.change_button_action)
        layout.add_widget(change_button)

        return layout

    def default_action(self, instance):
        self.label.text = "Default Action Triggered!"

    def custom_action(self, instance):
        self.label.text = "Custom Action Triggered!"

    def change_button_action(self, instance):
        # Change text and action of the dynamic button
        self.dynamic_button.text = "Custom Button"
        self.dynamic_button.unbind(on_press=self.default_action)
        self.dynamic_button.bind(on_press=self.custom_action)

if __name__ == '__main__':
    MainApp().run()

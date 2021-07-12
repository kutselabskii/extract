from kivy.app import App
from kivy.uix.widget import Widget

class MainScreen(Widget):
    def parse(self):
        text = self.ids.input.text
        numbers = text.replace(',', ' ').split()
        filenames = list(map(lambda x: self.ids.template.text.replace('*', x), numbers))

        self.ids.parsed.text = '\n'.join(filenames)

class ExtractApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    ExtractApp().run()
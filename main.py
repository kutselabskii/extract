from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.utils import platform

import os

class FolderSelector(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FolderSelector, self).__init__(**kwargs)
        self.drives_list.adapter.bind(on_selection_change=self.drive_selection_changed)

    def is_dir(self, directory, filename):
        return os.path.isdir(os.path.join(directory, filename))

    def get_win_drives(self):
            if platform == 'win':
                import win32api

                drives = win32api.GetLogicalDriveStrings()
                drives = drives.split('\000')[:-1]

                return drives
            else:
                return []

    def drive_selection_changed(self, *args):
        self.file_chooser.path = args[0].selection[0].text

class MainScreen(Widget):
    def parse(self):
        text = self.ids.input.text
        numbers = text.replace(',', ' ').split()
        filenames = list(map(lambda x: self.ids.template.text.replace('*', x), numbers))

        self.ids.parsed.text = '\n'.join(filenames)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_source_selector(self):
        content = FolderSelector(load=self.select_source, cancel=self.dismiss_popup)
        self._popup = Popup(title="Select source folder", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def select_source(self, path, filename):
        print(path, filename)

        self.dismiss_popup()

    def select_target(self, path, filename):
        pass

class ExtractApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    ExtractApp().run()
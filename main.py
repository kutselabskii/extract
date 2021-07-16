from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.utils import platform

import os
from pathlib import Path
from shutil import copy2
import codecs

class FolderSelector(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FolderSelector, self).__init__(**kwargs)

        for drive in self.get_win_drives():
            btn = Button(text=drive, size_hint_y=None, height=20)
            btn.bind(on_release=lambda btn: self.drive_selection_changed(btn.text))

            self.ids.drop.add_widget(btn)

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

    def drive_selection_changed(self, text):
        self.ids.drop.select(text)
        self.ids.chooser.path = text

class MainScreen(Widget):
    sourcePath = ""
    targetPath = ""
    filenames = []

    def parse(self):
        text = self.ids.input.text
        numbers = text.replace(',', ' ').split()
        self.filenames = list(filter(None, map(lambda x: self.ids.template.text.replace('*', x), numbers)))

        self.ids.parsed.text = '\n'.join(self.filenames)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_source_selector(self):
        content = FolderSelector(load=self.select_source, cancel=self.dismiss_popup)
        self._popup = Popup(title="Select source folder", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_target_selector(self):
        content = FolderSelector(load=self.select_target, cancel=self.dismiss_popup)
        self._popup = Popup(title="Select target folder", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def select_source(self, path, filename):
        self.sourcePath = path
        self.ids.sourceLabel.text = path

        self.dismiss_popup()

    def select_target(self, path, filename):
        self.targetPath = path
        self.ids.targetLabel.text = path

        self.dismiss_popup()

    def extract(self):
        for file in self.filenames:
            path = Path(self.sourcePath).joinpath(file)
            copy2(path, self.targetPath)

class ExtractApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    ExtractApp().run()
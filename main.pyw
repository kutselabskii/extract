from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.utils import platform
from plyer import filechooser

import os
import sys
import re
from pathlib import Path
from shutil import copy2
import logging

logger = None

def initLogging():
    global logger

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    fh = logging.FileHandler('log.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(stdout_handler)

class MainScreen(Widget):
    sourcePath = ""
    targetPath = ""
    filenames = []

    def parse(self):
        text = self.ids.input.text
        lines = text.replace(',', ' ').split()
        numbers = []
        for line in lines:
            search = re.match(r'\d{4}', line)
            if search is not None:
                numbers.append(self.ids.template.text.replace('*', search.group(0)))

        self.filenames = numbers

        self.ids.parsed.text = '\n'.join(self.filenames)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_source_selector(self):
        paths = filechooser.choose_dir(title="Select target folder")
        if len(paths) > 0:
            path = paths[0]
            self.sourcePath = path
            self.ids.sourceLabel.text = path

    def show_target_selector(self):
        paths = filechooser.choose_dir(title="Select target folder")
        if len(paths) > 0:
            path = paths[0]
            self.targetPath = path
            self.ids.targetLabel.text = path

    def extract(self):
        progressBar = self.ids.progress
        progressBar.value = 0
        progressBar.max = len(self.filenames)

        for i, photo in enumerate(self.filenames):
            progressBar.value = i + 1
            path = Path(self.sourcePath).joinpath(photo)
            if os.path.exists(path):
                copy2(path, self.targetPath)
            else:
                logger.warning(f"File {path} not found!")


class ExtractApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    initLogging()
    try:
        ExtractApp().run()
    except Exception as e:
        logger.critical(e)

from pathlib import Path
from utils.appdata import Settings

file_extentions = ['.mp3']

class MusicClass():
    def __init__(self):
        self.files: list[Path] = []

    def load(self):
        files = []
        for file in Path(Settings.music_dir).rglob('*'):
            if file.suffix in file_extentions:
                files.append(file)

        self.files = files

        return self

MusicFiles = MusicClass().load()
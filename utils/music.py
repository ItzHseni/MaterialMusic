from pathlib import Path
from utils.appdata import Settings
from tinytag import TinyTag, Image

file_extentions = ['.mp3']
class MusicFile():
    def __init__(self, title, artist, genre, cover_art, file_path):
        self.title: str = title
        self.artist: str = artist
        self.genre: str = genre
        self.cover_art: Image = cover_art
        self.file_path: Path = file_path

class MusicClass():
    def __init__(self):
        self.files: list[MusicFile] = []

    def load(self):
        files = []
        for file in Path(Settings.music_dir).rglob('*'):
            if file.suffix in file_extentions:
                tag = TinyTag.get(file, image=True)
                files.append(MusicFile(
                    title=tag.title,
                    artist=tag.artist,
                    genre=tag.genre,
                    cover_art=tag.images.any,
                    file_path=file
                ))

        self.files = files

        return self

MusicFiles = MusicClass().load()
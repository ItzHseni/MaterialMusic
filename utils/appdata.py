from pathlib import Path
from platformdirs import user_data_dir, user_cache_dir, user_config_dir
import json

APP = 'MaterialMusic'

data_dir = Path(user_data_dir(appname=APP))
cache_dir = Path(user_cache_dir(appname=APP))
config_dir = Path(user_config_dir(appname=APP))

data_dir.mkdir(exist_ok=True, parents=True)
cache_dir.mkdir(exist_ok=True, parents=True)
config_dir.mkdir(exist_ok=True, parents=True)

config_file = config_dir / 'config.json'

class SettingsClass():
    def __init__(self):

        self.music_dir: str = str(Path.home() / 'Music')
        self.dark_mode: bool = False

    def load(self):

        if config_file.is_file():

            attributes: dict = json.loads(config_file.read_text())

            for key, value in attributes.items():
                setattr(self, key, value)

        return self

    def save(self):

        attributes = vars(self)
        config_file.write_text(json.dumps(attributes, indent=2))

Settings = SettingsClass().load()
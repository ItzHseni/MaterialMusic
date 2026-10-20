from pathlib import Path
from platformdirs import user_data_dir, user_cache_dir, user_config_dir

APP = 'MaterialMusic'

data_dir = Path(user_data_dir(appname=APP))
cache_dir = Path(user_cache_dir(appname=APP))
config_dir = Path(user_config_dir(appname=APP))

data_dir.mkdir(exist_ok=True, parents=True)
cache_dir.mkdir(exist_ok=True, parents=True)
config_dir.mkdir(exist_ok=True, parents=True)

class Settings()
from pathlib import Path
from platformdirs import user_config_dir
import json
import flet as ft

APP = 'MaterialMusic'

config_dir = Path(user_config_dir(appname=APP))

config_dir.mkdir(exist_ok=True, parents=True)
print(config_dir)
config_file = config_dir / 'config.json'
theme_file = config_dir / 'current_theme.json'
user_theme_file = config_dir / 'user_theme.json'

default_theme = {
  "background": "#141218",
  "error": "#f2b8b5",
  "error_container": "#8c1d18",
  "inverse_on_surface": "#322f35",
  "inverse_primary": "#6750a4",
  "inverse_surface": "#e6e0e9",
  "on_background": "#e6e0e9",
  "on_error": "#601410",
  "on_error_container": "#f9dedc",
  "on_primary": "#381e72",
  "on_primary_container": "#eaddff",
  "on_primary_fixed": "#21005d",
  "on_primary_fixed_variant": "#4f378b",
  "on_secondary": "#332d41",
  "on_secondary_container": "#e8def8",
  "on_secondary_fixed": "#1d192b",
  "on_secondary_fixed_variant": "#4a4458",
  "on_surface": "#e6e0e9",
  "on_surface_variant": "#cac4d0",
  "on_tertiary": "#492532",
  "on_tertiary_container": "#ffd8e4",
  "on_tertiary_fixed": "#31111d",
  "on_tertiary_fixed_variant": "#633b48",
  "outline": "#938f99",
  "outline_variant": "#49454f",
  "primary": "#d0bcff",
  "primary_container": "#4f378b",
  "primary_fixed": "#eaddff",
  "primary_fixed_dim": "#d0bcff",
  "scrim": "#000000",
  "secondary": "#ccc2dc",
  "secondary_container": "#4a4458",
  "secondary_fixed": "#e8def8",
  "secondary_fixed_dim": "#ccc2dc",
  "shadow": "#000000",
  "surface": "#141218",
  "surface_bright": "#3b383e",
  "surface_container": "#211f26",
  "surface_container_high": "#2b2930",
  "surface_container_highest": "#36343b",
  "surface_container_low": "#1d1b20",
  "surface_container_lowest": "#0f0d13",
  "surface_dim": "#141218",
  "surface_tint": "#d0bcff",
  "surface_variant": "#49454f",
  "tertiary": "#efb8c8",
  "tertiary_container": "#633b48",
  "tertiary_fixed": "#ffd8e4",
  "tertiary_fixed_dim": "#efb8c8"
}

class SettingsClass():
    def __init__(self):

        self.music_dir: str = str(Path.home() / 'Music')
        self.dark_mode: bool = False
        self.use_wallpaper: bool = True
        self.use_default_theme: bool = False
        self.use_custom_theme: bool = True

    def load(self):

        if config_file.is_file():

            attributes: dict = json.loads(config_file.read_text())

            for key, value in attributes.items():
                setattr(self, key, value)

        return self

    def save(self):

        attributes = vars(self)
        config_file.write_text(json.dumps(attributes, indent=2))

class ThemeClass():
    def __init__(self):
        self.default: dict = default_theme
        self.user_theme: dict = default_theme
        self.theme: dict = default_theme

    def load(self):
         
        if theme_file.is_file():
            theme: dict = json.loads(theme_file.read_text())
            self.theme = theme
        else:
            theme_file.write_text(json.dumps(default_theme, indent=2))
      
        if user_theme_file.is_file():
            theme: dict = json.loads(user_theme_file.read_text())
            self.user_theme = theme
        else:
            user_theme_file.write_text(json.dumps(self.user_theme, indent=2))
            
        return self

    def save(self):

        theme_file.write_text(json.dumps(self.theme, indent=2))
        user_theme_file.write_text(json.dumps(self.user_theme, indent=2))

Settings = SettingsClass().load()
Theme = ThemeClass().load()
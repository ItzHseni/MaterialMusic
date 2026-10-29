from pathlib import Path
import flet as ft
import json
from utils.appdata import Theme, Settings

LINUX_COLOUR_FILE = Path('~/.local/state/quickshell/user/generated/colors.json').expanduser()

class MaterialTheme():
    def __init__(self):
        self.theme: ft.Theme = None

    def load(self):

        if Settings.use_wallpaper:
            if LINUX_COLOUR_FILE.exists():
                data = json.loads(LINUX_COLOUR_FILE.read_text())
        else:
            if Settings.use_default_theme:
                data = Theme.default
            else:
                data = Theme.theme
            
        theme = ft.Theme(
            use_material3=True,
            color_scheme=ft.ColorScheme(
                primary=data['primary'],
                on_primary=data['on_primary'],
                primary_container=data['primary_container'],
                on_primary_container=data['on_primary_container'],
                secondary=data['secondary'],
                on_secondary=data['on_secondary'],
                secondary_container=data['secondary_container'],
                on_secondary_container= data['on_secondary_container'],
                tertiary=data['tertiary'],
                on_tertiary=data['on_tertiary'],
                tertiary_container=data['tertiary_container'],
                on_tertiary_container=data['on_tertiary_container'],
                error=data['error'],
                on_error=data['on_error'],
                error_container=data['error_container'],
                on_error_container=data['on_error_container'],
                surface=data['surface'],
                on_surface=data['on_surface'],
                on_surface_variant=data['on_surface_variant'],
                outline=data['outline'],
                outline_variant=data['outline_variant'],
                shadow=data['shadow'],
                scrim=data['scrim'],
                inverse_surface=data['inverse_surface'],
                on_inverse_surface=data['inverse_on_surface'],
                inverse_primary=data['inverse_primary'],
                surface_tint=data['surface_tint'],
                on_primary_fixed=data['on_primary_fixed'],
                on_secondary_fixed=data['on_secondary_fixed'],
                on_tertiary_fixed=data['on_tertiary_fixed'],
                on_primary_fixed_variant=data['on_primary_fixed_variant'],
                on_secondary_fixed_variant=data['on_secondary_fixed_variant'],
                on_tertiary_fixed_variant=data['on_tertiary_fixed_variant'],
                primary_fixed=data['primary_fixed'],
                secondary_fixed=data['secondary_fixed'],
                tertiary_fixed=data['tertiary_fixed'],
                primary_fixed_dim=data['primary_fixed_dim'],
                secondary_fixed_dim=data['secondary_fixed_dim'],
                surface_bright=data['surface_bright'],
                surface_container=data['surface_container'],
                surface_container_high=data['surface_container_high'],
                surface_container_highest=data['surface_container_highest'],
                surface_container_low=data['surface_container_low'],
                surface_container_lowest=data['surface_container_lowest'],
                surface_dim=data['surface_dim'],
                tertiary_fixed_dim=data['tertiary_fixed_dim'],
            )
        )

        self.theme = theme

        return self

MaterialYou = MaterialTheme().load()
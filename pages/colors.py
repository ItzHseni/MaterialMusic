import flet as ft
from utils.appdata import Settings, Theme
from utils.music import MusicFiles
from utils.theme import MaterialYou
from flet_color_pickers import HueRingPicker

GROUPS = theme_groups = {
    'Primary': [
        'primary',
        'on_primary',
        'primary_container',
        'on_primary_container',
        'inverse_primary',
        'surface_tint',
    ],

    'Secondary': [
        'secondary',
        'on_secondary',
        'secondary_container',
        'on_secondary_container',
    ],

    'Tertiary': [
        'tertiary',
        'on_tertiary',
        'tertiary_container',
        'on_tertiary_container',
    ],

    'Error': [
        'error',
        'on_error',
        'error_container',
        'on_error_container',
    ],

    'Surface': [
        'surface',
        'on_surface',
        'on_surface_variant',
        'inverse_surface',
        'inverse_on_surface',
        'surface_bright',
        'surface_container',
        'surface_container_high',
        'surface_container_highest',
        'surface_container_low',
        'surface_container_lowest',
        'surface_dim',
    ],

    'Outline': [
        'outline',
        'outline_variant',
    ],

    'Primary Fixed': [
        'primary_fixed',
        'primary_fixed_dim',
        'on_primary_fixed',
        'on_primary_fixed_variant',
    ],

    'Secondary Fixed': [
        'secondary_fixed',
        'secondary_fixed_dim',
        'on_secondary_fixed',
        'on_secondary_fixed_variant',
    ],

    'Tertiary Fixed': [
        'tertiary_fixed',
        'tertiary_fixed_dim',
        'on_tertiary_fixed',
        'on_tertiary_fixed_variant',
    ],

    'Utility': [
        'shadow',
        'scrim',
    ],
}

def setting_group(title: str, settings: list[ft.ListTile]) -> ft.Control:
    return ft.Column(
        spacing=10,
        controls=[
            ft.Text(value=title, color=ft.Colors.PRIMARY, weight=ft.FontWeight.BOLD, size=15),

            ft.Card(
                content=ft.Column(controls=settings),
                bgcolor=ft.Colors.SURFACE_CONTAINER
            )
        ]
    )

def build(page: ft.Page) -> ft.Control:

    def circle_hover(event: ft.Event[ft.Container]):
        control = event.control
        control.scale = 1.1 if event.data else 1
        return

    def colour_circle(event: ft.Event[ft.Container]):

        new_colour_container = ft.Container(
            bgcolor=Theme.theme[event.control.data],
            expand=True
        )

        def change_colour(event: ft.Container[HueRingPicker]):
            new_colour_container.bgcolor = event.data
            return

        def close_popup(event: ft.Event):
            event.page.pop_dialog()

        def save_colour():
            Theme.theme[event.control.data] = new_colour_container.bgcolor
            event.control.bgcolor = Theme.theme[event.control.data]

            page.theme = MaterialYou.load().theme
            page.update()
            
            event.page.pop_dialog()

        event.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Pick Colour"),
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                content=ft.Column(
                    controls=[
                        HueRingPicker(
                            color=Theme.theme[event.control.data],
                            on_color_change=change_colour
                        ),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    bgcolor=Theme.theme[event.control.data],
                                    expand=True
                                ),
                                new_colour_container
                            ],
                            expand=True
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    width=1000
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=close_popup),
                    ft.FilledButton("Save", on_click=save_colour),
                ],
            )
        )

    color_controls = []
    for key in GROUPS.keys():
        sub_colors = []
        for sub_color in GROUPS[key]:
            title = sub_color.replace('_', ' ').title()
            list_tile = ft.ListTile(
                title=title,
                trailing=ft.Container(
                    ink=True,
                    height=32,
                    width=32,
                    border_radius=16,
                    bgcolor=Theme.theme[sub_color],
                    on_click=colour_circle,
                    on_hover=circle_hover,
                    data=sub_color
                )
            )
            sub_colors.append(list_tile)

        color_type = setting_group(
            title=key,
            settings=sub_colors
        )

        color_controls.append(color_type)

    return ft.Container(
        padding=16,
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
            ft.Text(value='Edit Theme', size=32, weight=ft.FontWeight.BOLD),

            ft.Container(height=18),

            ft.ListView(
                spacing=16,
                controls=color_controls,
                expand=True,
                padding=ft.Padding.only(right=16)
            ),
        ]))
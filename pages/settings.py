import flet as ft
from utils.appdata import Settings
from utils.music import MusicFiles
from utils.theme import MaterialYou

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

    async def pick_mf():
        path = await ft.FilePicker().get_directory_path()
        if path:
            mf_path.content = path
            Settings.music_dir = path
            MusicFiles.load()
            page.pubsub.send_all_on_topic('mfiles_changed', None)

    def toggle_mode(event: ft.Event[ft.Switch]):
        page: ft.Page = event.control.page

        if event.control.value:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT

        Settings.dark_mode = False

        page.update()

    def refresh_theme():
        page.theme = MaterialYou.load().theme
        page.update()

    def refresh_files():
        MusicFiles.load()
        page.pubsub.send_all_on_topic('mfiles_changed', None)

    def use_wallpaper(event: ft.Event[ft.Switch]):
        Settings.use_wallpaper = event.control.value
        default_col_tile.disabled = event.control.value
        default_col_tile.trailing.value = not event.control.value
        edit_col_tile.disabled = default_col_tile.disabled or default_col_tile.trailing.value
        refresh_theme()

    def default_colours(event: ft.Event[ft.Switch]):
        Settings.use_default_theme = event.control.value
        edit_col_tile.disabled = event.control.value or default_col_tile.disabled
        refresh_theme()

    def edit_colours():
        page.pubsub.send_all_on_topic('edit_colours', None)
        return

    mf_path = ft.TextButton(icon=ft.Icons.FOLDER, content=Settings.music_dir, on_click=pick_mf)

    default_col_tile = ft.ListTile(
        title='Default Colours',
        leading=ft.Icons.FACTORY,
        trailing=ft.Switch(value=Settings.use_default_theme, on_change=default_colours),
        disabled=Settings.use_wallpaper
    )

    edit_col_tile = ft.ListTile(
        title='Customer Colours',
        leading=ft.Icons.EDIT,
        trailing=ft.FilledButton(content='Edit', on_click=edit_colours),
        disabled=Settings.use_default_theme or Settings.use_wallpaper
    )


    return ft.Container(
        padding=16,
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
            ft.Text(value='Settings', size=32, weight=ft.FontWeight.BOLD),

            ft.Container(height=18),

            ft.Column(
                spacing=16,
                controls=[

                    setting_group(title='Appearance', settings=[
                        ft.ListTile(
                            title='Dark Mode',
                            leading=ft.Icons.DARK_MODE,
                            trailing=ft.Switch(value=Settings.dark_mode, on_change=toggle_mode)
                        ),
                        ft.ListTile(
                            title='Material Theme',
                            leading=ft.Icons.COLOR_LENS,
                            trailing=ft.IconButton(icon=ft.Icon(ft.Icons.REFRESH),on_click=refresh_theme)
                        ),
                        ft.ListTile(
                            title='Wallpaper Colours',
                            leading=ft.Icons.WALLPAPER,
                            trailing=ft.Switch(value=Settings.use_wallpaper, on_change=use_wallpaper)
                        ),
                        default_col_tile,
                        edit_col_tile
                    ]),
                    setting_group(title='Folders', settings=[
                        ft.ListTile(
                            title='Music Folder',
                            leading=ft.Icons.FOLDER,
                            trailing=mf_path
                        ),
                        ft.ListTile(
                            title='Refresh Files',
                            leading=ft.Icons.MUSIC_NOTE,
                            trailing=ft.IconButton(icon=ft.Icon(ft.Icons.REFRESH),on_click=refresh_files)
                        ),
                    ]),
                    setting_group(title='About', settings=[
                        ft.ListTile(
                            title='MaterialMusic',
                            subtitle='Version 1.0',
                            leading=ft.Icons.INFO_OUTLINE,
                        )
                    ])
                ]
            ),
        ]))
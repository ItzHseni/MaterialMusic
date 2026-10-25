import flet as ft
from utils.appdata import Settings
from utils.music import MusicFiles

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
            Settings.dark_mode = True

        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            Settings.dark_mode = False

        page.update()

    mf_path = ft.TextButton(icon=ft.Icons.FOLDER, content=Settings.music_dir, on_click=pick_mf)

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
                    ]),
                    setting_group(title='Folders', settings=[
                        ft.ListTile(
                            title='Music Folder',
                            leading=ft.Icons.MUSIC_NOTE,
                            trailing=mf_path
                        )
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
import flet as ft
from utils.music import MusicFiles, MusicFile

def cover_art(file: MusicFile):
    if file.cover_art:
        return ft.Container(
            content=ft.Image(
                src=file.cover_art.data,
                width=64,
                height=64,
                border_radius=10,
                fit=ft.BoxFit.COVER
            )
        )

    return ft.Container(
        content=ft.Icon(icon=ft.Icons.MUSIC_NOTE, color=ft.Colors.ON_PRIMARY_CONTAINER),
        width=64,
        height=64,
        border_radius=10,
        bgcolor=ft.Colors.PRIMARY_CONTAINER
    )

def build() -> ft.Control:

    def dum():
        return
    cards = []

    def on_click(event: ft.Event[ft.Container]):
        file: MusicFile = event.control.data
        file_title = file.title if file.title else file.file_path.stem
        file_artist = file.artist if file.artist else ''
        
        title = ft.TextField(label='Song Title', value=file_title)
        artist = ft.TextField(label='Artist Name', value=file_artist)

        event.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Edit tags"),
                content=ft.Column(
                    controls=[title, artist],
                    width=1000
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=dum()),
                    ft.FilledButton("Save", on_click=dum()),
                ],
            )
        )
        return
    
    for file in MusicFiles.files:
        cards.append(
            ft.Container(
                ink=True,
                on_click=on_click,
                border_radius=16,
                padding=16,
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                data=file,
                content=ft.Row(
                    spacing=16,
                    controls=[
                        cover_art(file=file),
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    value=file.title if file.title else file.file_path.name,
                                    size=16,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Text(
                                    value=file.artist if file.artist else 'Unknown Artist',
                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                    size=13
                                )
                            ]
                        )
                    ]
                )
            )
        )

    return ft.Container(
        padding=24,
        content=ft.ListView(
            controls=cards,
            spacing=8,
            expand=True
        )
    )
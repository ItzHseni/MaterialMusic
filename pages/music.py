import flet as ft
from utils.music import MusicFiles, MusicFile

def cover_art(file: MusicFile):

    if file.cover_bytes:
        return ft.Container(
            content=ft.Image(
                src=file.cover_bytes,
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

def music_card(file: MusicFile, on_click):

    return (
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
                            value=file.title if file.title else file.file_path.stem,
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

def build(page: ft.Page) -> ft.Control:

    def dum():
        return

    def mfiles_changed(topic, message):
        x = [music_card(file=file, on_click=on_click) for file in MusicFiles.files]
        music_list.controls = x

    def on_click(event: ft.Event[ft.Container]):
        return

    page.pubsub.subscribe_topic('mfiles_changed', mfiles_changed)

    cards = [music_card(file=file, on_click=on_click) for file in MusicFiles.files]
    music_list = ft.ListView(
        controls=cards,
        spacing=8,
        expand=True
    )

    return ft.Container(
        padding=24,
        content=ft.Column(
            controls=[music_list]
        )
    )
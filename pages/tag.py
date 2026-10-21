import flet as ft
from utils.music import MusicFiles

def build() -> ft.Control:
    cards = []

    def on_click():
        return
    
    for file in MusicFiles.files:
        cards.append(
            ft.Container(
                ink= True,
                on_click=on_click,
                border_radius=15,
                padding=16,
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                content=ft.Column(
                    spacing=5,
                    controls=[
                        ft.Text(file.name),
                        ft.Text('Unkown Artist')
                    ]
                )
            )
        )

    return ft.Container(
        padding=40,
        content=ft.ListView(
            controls=cards,
            spacing=5,
            expand=True
        )
    )
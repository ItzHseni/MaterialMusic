import flet as ft
from utils.music import MusicFiles

def build() -> ft.Control:
    cards = []

    def on_click():
        return
    
    for file in MusicFiles.files:
        cards.append(
            ft.Container(
                ink=True,
                on_click=on_click,
                border_radius=16,
                padding=16,
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                content=ft.Row(
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    value=file.title if file.title else file.file_path.name,
                                    size=16,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Text(
                                    value=file.artist if file.artist else 'Unkown Artist',
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
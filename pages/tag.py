import flet as ft
from utils.music import MusicFiles, MusicFile
from utils.metadata import get_recordings

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

    def close_popup(event: ft.Event):
        event.page.pop_dialog()

    def on_click(event: ft.Event[ft.Container]):
        file: MusicFile = event.control.data
        file_title = file.title if file.title else file.file_path.stem
        file_artist = file.artist if file.artist else ''
        
        title_field = ft.TextField(label='Song Title', value=file_title)
        artist_field = ft.TextField(label='Artist Name', value=file_artist)
        song_row = ft.Row(controls=[], spacing=20, scroll=ft.ScrollMode.AUTO, height=152, vertical_alignment=ft.CrossAxisAlignment.START)

        def on_rclick(event: ft.Event[ft.Container]):
            rec = event.control.data

            title_field.value = rec['title']
            artist_field.value = ' ,'.join(rec['artists'])

        def search_recordings():
            song_title = title_field.value
            song_artist = artist_field.value

            recordings = get_recordings(song=song_title, artist=song_artist)

            song_row.controls.clear()

            for recording in recordings:
                song_row.controls.append(
                    ft.Container(
                        ink=True,
                        on_click=on_rclick,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                        width=128,
                        height=128,
                        border_radius=20,
                        padding=15,
                        content=ft.Column(
                            controls=[
                                ft.Text(value=recording['title'], overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(value=' ,'.join(recording['artists']), overflow=ft.TextOverflow.ELLIPSIS)
                            ]
                        ),
                        data=recording
                        
                    )
                )

        event.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Edit tags"),
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                content=ft.Column(
                    controls=[
                        title_field,
                        artist_field,
                        ft.FilledButton(icon=ft.Icons.SEARCH, on_click=search_recordings, content='Search'),
                        ft.Column(height=12),
                        song_row
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    width=1000
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=close_popup),
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
import flet as ft
from utils.music import MusicFiles, MusicFile
from utils.metadata import get_recordings, get_recording, write_recording
import asyncio
from tinytag import Image

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

        music_list_card = event.control

        def on_field_change(event: ft.Event[ft.TextField]):

            value = event.control.value

            if event.control.label == 'Song Title':
                file.title = value
                card_container.content.content.controls[1].controls[0].value = file.title if file.title else file.file_path.stem

            elif event.control.label == 'Artist Name':
                file.artist = value
                card_container.content.content.controls[1].controls[1].value = file.artist if file.artist else 'Unknown Artist'

            elif event.control.label == 'Tags':
                file.genre = value
            elif event.control.label == 'Release Date':
                file.release_date = value

        cancelled = False
        file: MusicFile = event.control.data
        file_title = file.title if file.title else file.file_path.stem
        file_artist = file.artist if file.artist else None

        card_container = ft.Container(content=music_card(file=file, on_click=dum))
        title_field = ft.TextField(label='Song Title', value=file_title, expand=True, height=1, on_change=on_field_change)
        artist_field = ft.TextField(label='Artist Name', value=file_artist, hint_text='Albert Einstien', expand=True, height=1, on_change=on_field_change)
        tags_field = ft.TextField(label='Tags', value=None, hint_text='Pop', expand=True, on_change=on_field_change)
        album_field = ft.TextField(label='Album Name', value=None, hint_text='Evil Noises', expand=True, on_change=on_field_change)
        album_artist = ft.TextField(label='Album Artist', value=None, hint_text='Robert Alan', expand=True, on_change=on_field_change)
        release_date = ft.TextField(label='Release Date', value=None, hint_text='6/7/2067', expand=True, on_change=on_field_change)

        song_row = ft.Row(controls=[], spacing=20, scroll=ft.ScrollMode.AUTO, height=152, vertical_alignment=ft.CrossAxisAlignment.START)
            
        def close_popup(event: ft.Event):
            nonlocal cancelled
            cancelled = True 
            event.page.pop_dialog()

        def save_metadata():
            write_recording(file=file)
            MusicFiles.load()
            index = music_list.controls.index(music_list_card)
            music_list.controls[index] = music_card(file=file, on_click=on_click)
            music_list.update()
            event.page.pop_dialog()

        def on_rclick(event: ft.Event[ft.Container]):
            rec = event.control.data
            
            file.title = title_field.value = rec['title']
            file.artist = artist_field.value = ', '.join(rec['artists'])
            file.genre = tags_field.value = ', '.join(rec['tags'])
            file.release_date = release_date.value = rec['release_date']
            file.cover_bytes = rec['cover_bytes']

            card_container.content = music_card(file=file, on_click=dum)

        async def search_recordings(event: ft.Event[ft.FilledButton]):
            nonlocal cancelled
            cancelled = False

            event.control.disabled = True
            event.control.update()
            song_title = title_field.value
            song_artist = artist_field.value

            try:
                recordings = await asyncio.to_thread(get_recordings, song=song_title, artist=song_artist)

                song_row.controls.clear()

                for recording in recordings:

                    if cancelled:
                        break

                    all_info = await asyncio.to_thread(get_recording, song=recording)
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
                            data=all_info
                            
                        )
                    )

                    if cancelled:
                        break
                    song_row.update()

            except RuntimeError:
                pass
            finally:
                try:
                    if not cancelled:
                        event.control.disabled = False
                        event.control.update()
                except RuntimeError:
                    pass

        event.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Edit tags"),
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                content=ft.Column(
                    controls=[
                        ft.Column(controls=[title_field, artist_field], height=150),
                        ft.Row(controls=[album_field, album_artist], spacing=10),
                        ft.Row(controls=[release_date, tags_field], spacing=10),
                        ft.FilledButton(icon=ft.Icons.SEARCH, on_click=search_recordings, content='Search'),
                        ft.Column(height=12),
                        song_row,
                        card_container
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    width=1000
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=close_popup),
                    ft.FilledButton("Save", on_click=save_metadata),
                ],
            )
        )
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
        content=music_list
    )
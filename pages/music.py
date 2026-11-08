import flet as ft
from utils.music import MusicFiles, MusicFile
from utils.player import start, play_index, toggle
from utils.player import player as mpv_player

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

    def music_select(event: ft.Event[ft.Container]):
        play_index(index=music_list.controls.index(event.control))
        return

    def mfiles_changed(topic, message):
        x = [music_card(file=file, on_click=music_select) for file in MusicFiles.files]
        start(files=MusicFiles)
        music_list.controls = x

    page.pubsub.subscribe_topic('mfiles_changed', mfiles_changed)

    cards = [music_card(file=file, on_click=music_select) for file in MusicFiles.files]
    start(files=MusicFiles)

    music_list = ft.ListView(
        controls=cards,
        spacing=8,
        expand=3
    )

    player_cover = ft.Container(
        content=ft.Icon(
            icon=ft.Icons.MUSIC_NOTE,
            size=96,
            color=ft.Colors.ON_PRIMARY_CONTAINER,
        ),
        border_radius=48,
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        height=256,
        width=256,
    )

    async def change_cover(file: MusicFile):
        if file.cover_bytes:
            player_cover.content = ft.Image(
                src=file.cover_bytes,
                width=256,
                height=256,
                fit=ft.BoxFit.COVER,
            )
        else:
            player_cover.content = ft.Icon(
                icon=ft.Icons.MUSIC_NOTE,
                size=96,
                color=ft.Colors.ON_PRIMARY_CONTAINER,
            )

        try:
            player_cover.update()
        except RuntimeError:
            pass

    def music_change(name, position):
        if (position == None) or (position < 0) or (position >= len(MusicFiles.files)):
            return
        
        page.run_task(change_cover, MusicFiles.files[position])

    mpv_player.observe_property("playlist-pos", music_change)

    pause_button = ft.FilledButton(
        content=ft.Icon(ft.Icons.PLAY_ARROW, color=ft.Colors.ON_PRIMARY_CONTAINER),
        expand=True,
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
    )

    player = ft.Container(
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        expand=1,
        padding=24,
        border_radius=28,
        content=ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(controls=[
                    ft.Icon(ft.Icons.MUSIC_NOTE, color=ft.Colors.PRIMARY),
                    ft.Text(value='Player', weight=ft.FontWeight.BOLD, size=24),
                ]),
                ft.Container(height=10),
                player_cover,
                ft.Column(height=67),
                ft.Row(controls=[
                    pause_button
                ])
            ],
        ),
    )

    return ft.Container(
        padding=24,
        content=ft.Row(
            spacing=16,
            controls=[
                music_list,
                player
            ]
        )
    )


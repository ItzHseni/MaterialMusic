import flet as ft
from pages import music, settings, tag, colors
from utils.appdata import Settings, Theme
from utils.theme import MaterialYou

# dont put pages after settings 
# and colors gotta be befofre settings
# settings gotta be the last index cuz ion wanna hardcode the index since it might get annoying to change later
# holy long comment
pages = [music,
         tag,
         colors,
         settings
         ]

SETTINGS_INDEX = len(pages) - 1

def main(page: ft.Page):

    if Settings.dark_mode:
        theme_mode = ft.ThemeMode.DARK
    else:
        theme_mode = ft.ThemeMode.LIGHT

    page.theme_mode = theme_mode

    page.theme = MaterialYou.theme
    page.bgcolor = ft.Colors.SURFACE

    async def on_window_event(event: ft.WindowEvent):
        if event.type == ft.WindowEventType.CLOSE:
            Settings.save()
            Theme.save()
            await page.window.destroy()

    page.window.prevent_close = True
    page.window.on_event = on_window_event

    builds = [p.build(page) for p in pages]

    body = ft.Container(content=builds[0], expand=True)

    def change_page(event: ft.ControlEvent):
        selected = event.control.selected_index
        body.content = builds[selected]

        if selected != SETTINGS_INDEX:
            settings_button.selected = False
            settings_button.bgcolor = None

        page.update()

    def edit_colors(topic, message):
        body.content = builds[len(builds)-2]
        page.update()

    def open_settings():
        rail.selected_index = None
        settings_button.selected = True
        settings_button.bgcolor = ft.Colors.SECONDARY_CONTAINER
        body.content = builds[SETTINGS_INDEX]
        page.update()

    page.pubsub.subscribe_topic('edit_colours', edit_colors)

    settings_button = ft.IconButton(icon=ft.Icons.SETTINGS, on_click=open_settings, selected_icon_color=ft.Colors.SECONDARY)

    rail = ft.NavigationRail(
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.MUSIC_NOTE, label='Music'),
            ft.NavigationRailDestination(icon=ft.Icons.TAG, label='Tags'),
        ],
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        on_change=change_page,
        trailing=ft.Container(content=settings_button, padding=ft.Padding.only(bottom=20)),
        pin_trailing_to_bottom=True,)

    page.add(ft.Row(controls=[rail, ft.VerticalDivider(thickness=2), body], expand=True))

ft.run(main)
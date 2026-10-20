import flet as ft
from pages import home, settings, tag

# dont put pages after settings 
# settings gotta be the last index cuz ion wanna hardcode the index since it might get annoying to change later
# holy long comment
pages = [home,
         tag,
         settings
         ]

SETTINGS_INDEX = len(pages) - 1

def main(page: ft.Page):

    builds = [p.build() for p in pages]

    body = ft.Container(content=builds[SETTINGS_INDEX], expand=True)

    def change_page(event: ft.ControlEvent):
        selected = event.control.selected_index
        body.content = builds[selected]

        if selected != SETTINGS_INDEX:
            settings_button.selected = False
            settings_button.bgcolor = None

        page.update()

    def open_settings():
        rail.selected_index = None
        settings_button.selected = True
        settings_button.bgcolor = ft.Colors.SECONDARY_CONTAINER
        body.content = builds[SETTINGS_INDEX]
        page.update()

    settings_button = ft.IconButton(icon=ft.Icons.SETTINGS, on_click=open_settings, selected_icon_color=ft.Colors.SECONDARY)

    rail = ft.NavigationRail(
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME, label='Home'),
            ft.NavigationRailDestination(icon=ft.Icons.TAG, label='Tags')
        ],
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        on_change=change_page,
        trailing=ft.Container(content=settings_button, padding=ft.Padding.only(bottom=20)),
        pin_trailing_to_bottom=True,)

    page.add(ft.Row(controls=[rail, ft.VerticalDivider(thickness=2), body], expand=True))

ft.run(main)
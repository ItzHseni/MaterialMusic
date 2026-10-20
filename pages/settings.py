import flet as ft

def setting_group(title: str, settings: list[ft.ListTile]) -> ft.Control:
    return ft.Column(
        spacing=5,
        controls=[
            ft.Text(title),

            ft.Card(
                content=ft.Column(controls=settings),
                bgcolor=ft.Colors.SURFACE_CONTAINER
            )
        ]
    )

def build() -> ft.Control:

    return ft.Container(
        padding=16,
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
            ft.Text(value='Settings', size=32, weight=ft.FontWeight.BOLD),

            ft.Column(
                spacing=16,
                controls=[
                    setting_group(title='Test', settings=[
                        ft.ListTile(title='test til',
                                    leading=ft.Icons.ABC)
                    ])
                ]
            ),
        ]))
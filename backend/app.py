import flet as ft


def main(page: ft.Page):
    page.title = 'FaceLock'
    page.bgcolor = '#ffffff'
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                        ft.Button(content="Enabled button"),
                        ft.Button(content="Disabled button", disabled=True),
                    ]
                )
            )
        )
    page.update()
ft.app(target=main)


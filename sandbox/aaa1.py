import flet as ft


def main(page: ft.Page):
    page.title = "FaceLock"

    def route_change(e):
        page.views.clear()

        page.views.append(
            ft.View(
                '/',
                [
                    ft.Column(
                        [
                            ft.Text("Welcome to FaceLock!"),
                            ft.ElevatedButton("Go to Login", on_click=lambda e: page.go('/login')),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ],
            )
        )

        if page.route == '/login':
            page.views.append(
                ft.View(
                    '/login',
                    [
                        ft.Text("Login Page"),
                        ft.ElevatedButton("Back to Home", on_click=lambda e: page.go('/')),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main, view=ft.FLET_APP)
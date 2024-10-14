import flet as ft
def edit_bills_page(current_theme, page:ft.Page, BASE_URL:str):
    appbar = ft.AppBar(leading=ft.Row(controls=[ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=current_theme["top_appbar_colors"]["icon_color"], on_click=lambda _: page.go("/")),ft.Image(src=current_theme["top_appbar_colors"]["icon"], fit=ft.ImageFit.CONTAIN)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"])
        
    return ft.View(
        "/edit_bills",
                    [
                        ft.Text("This page is comming soon")
                    ],
                    appbar=appbar
                )
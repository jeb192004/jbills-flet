import flet as ft
from urllib.parse import urlencode
import os

from ui.login_ui import login_page
from ui.bills_ui import bills_page
from ui.home_ui import home_page
from ui.settings_ui import settings_page
from ui.pay_ui import pay_page
from ui.edit_bills_ui import edit_bills_page
from ui.theme import light_theme, dark_theme, green_theme
from ui.charts_ui import charts_page

BASE_URL = 'https://j-bills.com/'
#BASE_URL = 'http://localhost:1338/'


def main(page: ft.Page):
    page.title = "j-bills"
    if page.platform is not page.platform.ANDROID:
        page.window.width = 400
    #page.platform = ft.PagePlatform.ANDROID

    user_info = {}
    user_id = page.client_storage.get("burnison.me.user.id")
    

    def route_change(route):
        saved_theme = page.client_storage.get("burnison.me.current.theme")
        current_theme = None
        if saved_theme == "light" or saved_theme is None:
            current_theme = light_theme()
        elif saved_theme == "dark":
            current_theme = dark_theme()
        elif saved_theme == "green":
            current_theme = green_theme()

        page.views.clear()
        #page.views.append(home_page(page, BASE_URL))
        bills_page(current_theme,page, BASE_URL, user_id)
        if page.route == "/login":
            page.views.clear()
            page.views.append(login_page(current_theme, page, BASE_URL))
        elif page.route == "/bills":
            bills_page(current_theme, page, BASE_URL, user_id)
        elif page.route == "/edit_bills":
            page.views.append(edit_bills_page(current_theme, page, BASE_URL))
        elif page.route == "/charts":
            page.views.append(charts_page(current_theme, page, BASE_URL, user_id))
        elif page.route == "/pay":
            page.views.append(pay_page(current_theme, page, BASE_URL))
        elif page.route == "/settings":
            page.views.append(settings_page(current_theme, page, BASE_URL))
        
        page.update()

    def view_pop(view):
        
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    if user_id is None:
        page.go('/login')
    else:
        print(f'Welcome, user {user_id}')
        page.go(page.route)


ft.app(main)
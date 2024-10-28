import flet as ft
import datetime

from data.bills import get_bills
#from ui.alert import create_loader, show_loader, hide_loader


def edit_bills_page(current_theme, page:ft.Page, BASE_URL:str, user_id:str):
    #bills = Bills(page, BASE_URL)
    #loader = create_loader()
    
    data = get_bills(page, user_id, BASE_URL)
    if data['error'] is None or data['error'] == "":
        profile_pic = data["profile_pic"]
        user_pay_hours = data["user_pay_hours"]
        my_bills = data["my_bills"]
        unpaid_bills = data["unpaid_bills"]

    date_text = ft.Text(value="Date: ", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"])
    def handle_change(e):
        print(f"Date changed: {e.control.value.strftime('%Y-%m-%d')}")
        date_text.value = f"Date: {e.control.value.strftime('%Y-%m-%d')}"
        page.update()
    def handle_dismissal(e):
        print(f"DatePicker dismissed")

    def open_date_picker(e, date_picker: ft.DatePicker):
        date_picker.pick_date()

    '''define controls here'''
    date_picker = ft.DatePicker(first_date=datetime.datetime.now(),
                                #last_date=datetime.datetime(year=2024, month=10, day=1),
                                on_change=handle_change,
                                on_dismiss=handle_dismissal,
                                )
    name_text = ft.TextField(label="Company/Person/Name: ", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    amount_due = ft.TextField(label="Amount Due: ", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    website = ft.TextField(label="Website(optional): ", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    phone_number = ft.TextField(label="Phone Number(optional): ", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    email = ft.TextField(label="Email(optional): ", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    due_date_picker = ft.ElevatedButton("Pick date",icon=ft.icons.CALENDAR_MONTH,
                                        on_click=lambda e: open_date_picker(e, date_picker=date_picker),
                                                    bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"]
                                                    )
    due_date_column = ft.Row(controls=[ft.Column(controls=[due_date_picker, date_text], expand=True)], expand=True, visible=False)
    frequency_dropdown = ft.Dropdown(label="Frequency(how often bill is paid)",expand=True, bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))

    day_of_week_or_month_dropdown = ft.Dropdown(label="Day of Week or Month",expand=True, bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    week_of_month_dropdown = ft.Dropdown(label="Select a week of the month",expand=True, bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    day_of_week_dropdown = ft.Dropdown(label="Select a day of the week",expand=True, bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    day_of_week_row = ft.Row(controls=[ft.Column(controls=[week_of_month_dropdown,day_of_week_dropdown],expand=True)], expand=True,visible=False)
    day_of_month_dropdown = ft.Dropdown(label="Select a day of the month",expand=True, bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    for i in range(1,32):
        day_of_month_dropdown.options.append(ft.dropdown.Option(str(i)))
    day_of_month_row = ft.Row(controls=[day_of_month_dropdown,], expand=True,visible=False)
    montly_row = ft.Row(controls=[
        ft.Column(controls=[
            day_of_week_or_month_dropdown,day_of_week_row,day_of_month_row
            ],expand=True),
        ], expand=True,visible=False)
    


    def frequency_dropdown_change(e):
        print(e.control.value)
        if e.control.value == "Weekly":
            if due_date_column.visible == True:
                due_date_column.visible = False
            if montly_row.visible == True:
                montly_row.visible = False
        
        if e.control.value == "Monthly":
            if due_date_column.visible == True:
                due_date_column.visible = False
            if montly_row.visible == False:
                montly_row.visible = True

        if e.control.value == "One Time":
            due_date_column.visible = True
            if montly_row.visible == True:
                montly_row.visible = False

        page.update()

    def day_of_week_or_month_dropdown_change(e):
        print(e.control.value)
        if e.control.value == "Day of Week (Mon, Tues, ect.)":
            if day_of_week_row.visible == False:
                day_of_week_row.visible = True
            if day_of_month_row.visible == True:
                day_of_month_row.visible = False
        if e.control.value == "Day of Month (1st, 2nd, ect.)":
            if day_of_month_row.visible == False:
                day_of_month_row.visible = True
            if day_of_week_row.visible == True:
                day_of_week_row.visible = False
        page.update()

    
    
    frequency_dropdown.options=[
            ft.dropdown.Option("Monthly"),
            ft.dropdown.Option("Weekly"),
            ft.dropdown.Option("One Time"),
        ]
    frequency_dropdown.on_change=lambda e: frequency_dropdown_change(e)

    day_of_week_or_month_dropdown.options=[
            ft.dropdown.Option("Day of Week (Mon, Tues, ect.)"),
            ft.dropdown.Option("Day of Month (1st, 2nd, ect.)"),
        ]
    day_of_week_or_month_dropdown.on_change=lambda e: day_of_week_or_month_dropdown_change(e)

    week_of_month_dropdown.options=[
            ft.dropdown.Option("First Week of the Month"),
            ft.dropdown.Option("Second Week of the Month"),
            ft.dropdown.Option("Third Week of the Month"),
            ft.dropdown.Option("Fourth Week of the Month"),
        ]
    #week_of_month_dropdown.on_change=lambda e: week_of_month_dropdown_change(e)

    day_of_week_dropdown.options=[
            ft.dropdown.Option("Sunday"),
            ft.dropdown.Option("Monday"),
            ft.dropdown.Option("Tuesday"),
            ft.dropdown.Option("Wednesday"),
            ft.dropdown.Option("Thursday"),
            ft.dropdown.Option("Friday"),
            ft.dropdown.Option("Saturday"),
        ]
    #day_of_week_dropdown.on_change=lambda e: day_of_week_dropdown_change(e)


    due_date_container = ft.Container(
        content=ft.Column(
            controls=[due_date_column,
                      montly_row,
            ],
            expand=True,
        ),
        expand=True,
    )
    
    if profile_pic:
        appbar = ft.AppBar(leading=ft.Row(controls=[ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=current_theme["top_appbar_colors"]["icon_color"], on_click=lambda _: page.go("/")),ft.Image(src=current_theme["top_appbar_colors"]["icon"], width=200, fit=ft.ImageFit.FIT_WIDTH)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"], actions=[ft.Container(content=ft.Image(src=profile_pic, width=40, height=40), border_radius=50, margin=ft.margin.only(right=10))])
    else:
        appbar = ft.AppBar(leading=ft.Row(controls=[ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=current_theme["top_appbar_colors"]["icon_color"], on_click=lambda _: page.go("/")),ft.Image(src=current_theme["top_appbar_colors"]["icon"], width=200, fit=ft.ImageFit.FIT_WIDTH)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"])
    
    page.overlay.append(date_picker)
    page.views.append(ft.View("/charts",
                              [ft.Stack(
                                  controls=[ft.Column(controls=[
                                        name_text,
                                        frequency_dropdown,
                                        due_date_container,
                                        amount_due,
                                        website,
                                        phone_number,
                                        email,
                                        
                                      ],
                                      expand=True,
                                      horizontal_alignment="center",
                                      scroll=ft.ScrollMode.AUTO),
                                      #loader
                                      ],
                                    )
                                ],
                                appbar=appbar,
                                bgcolor=current_theme["background"]
                            )
                        )
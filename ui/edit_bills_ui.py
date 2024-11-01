import re
import flet as ft
import datetime

from data.bills import get_bills, add_update_bills
#from ui.alert import create_loader, show_loader, hide_loader


def edit_bills_page(current_theme, page:ft.Page, BASE_URL:str, user_id:str):
    #bills = Bills(page, BASE_URL)
    #loader = create_loader()
    new_update = "new"
    data = get_bills(page, user_id, BASE_URL)
    if data['error'] is None or data['error'] == "":
        profile_pic = data["profile_pic"]
        user_pay_hours = data["user_pay_hours"]
        my_bills = data["my_bills"]
        unpaid_bills = data["unpaid_bills"]

    date_text = ft.Text(bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"])
    def handle_change(e):
        print(f"Date changed: {e.control.value.strftime('%Y-%m-%d')}")
        date_text.value = f"{e.control.value.strftime('%Y-%m-%d')}"
        page.update()
    def handle_dismissal(e):
        print(f"DatePicker dismissed")

    def open_date_picker(e, date_picker: ft.DatePicker):
        date_picker.pick_date()

    def on_amount_due_change(e):
        # Get the current input value, strip $, and reformat
        current_value = e.control.value.replace(".", "").replace(",", "")
        
        # Allow only digits
        if not current_value.isdigit():
            e.control.value = f"{amount_due.value}"
            page.update()
            return

        # Limit to a maximum length for formatting (e.g., max $9999.99)
        max_length = 15  # For up to "100,000,000,000.00"
        if len(current_value) > max_length:
            current_value = current_value[-max_length:]

        # Convert to dollar-and-cents format
        if len(current_value) <= 2:
            dollars = "0"
            cents = current_value.zfill(2)
        else:
            dollars = current_value[:-2]
            cents = current_value[-2:]

        formatted_value = f"{int(dollars):,}.{cents}"

        # Update the text field with the formatted value
        amount_due.value = formatted_value
        page.update()

    '''define controls here'''
    date_picker = ft.DatePicker(first_date=datetime.datetime.now(),
                                #last_date=datetime.datetime(year=2024, month=10, day=1),
                                on_change=handle_change,
                                on_dismiss=handle_dismissal,
                                )
    error_text = ft.TextField(bgcolor=ft.colors.RED, color="white", visible=False)
    name_text = ft.TextField(label="Company/Person/Name: ", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    amount_due = ft.TextField(label="Amount Due: ", prefix_text="$", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]), on_change=on_amount_due_change)
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
        day_of_week_or_month_dropdown.value = None
        day_of_month_dropdown.value = None
        week_of_month_dropdown.value = None
        date_text.value = ""
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

    def save(e):
        date_to_save = ""
        if name_text.value == "":
            name_text.border_color = ft.colors.RED
            name_text.update()
            return
        else:
            name_text.border_color = None
            name_text.update()
        if frequency_dropdown.value is not None:
            frequency_dropdown.border_color = None
            frequency_dropdown.update()
            if frequency_dropdown.value == "Weekly":
                date_to_save = ""
            if frequency_dropdown.value == "One Time":
                if date_text.value != "":
                    date_text.bgcolor = current_theme["list_item_colors"]['base']
                    page.update()
                    date_to_save = date_text.value #format = 2024-11-05
                    print("date_to_save: ", date_to_save)
                else:
                    date_text.value = "Please select a due date"
                    date_text.bgcolor = ft.colors.RED
                    page.update()
                    return
            if frequency_dropdown.value == "Monthly":
                if day_of_week_or_month_dropdown.value is not None:
                    day_of_week_or_month_dropdown.border_color = None
                    day_of_week_or_month_dropdown.update()
                    if day_of_week_or_month_dropdown.value == "Day of Week (Mon, Tues, ect.)":
                        if week_of_month_dropdown.value is not None:
                            week_of_month_dropdown.border_color = None
                            week_of_month_dropdown.update()
                        else:
                            week_of_month_dropdown.border_color = ft.colors.RED
                            week_of_month_dropdown.update()
                            return
                        if day_of_week_dropdown.value is not None:
                            day_of_week_dropdown.border_color = None
                            day_of_week_dropdown.update()
                        else:
                            day_of_week_dropdown.border_color = ft.colors.RED
                            day_of_week_dropdown.update()
                            return
                        if week_of_month_dropdown.value and day_of_week_dropdown.value:
                            date_to_save = f"{week_of_month_dropdown.value.split()[0]}-{day_of_week_dropdown.value}"
                    if day_of_week_or_month_dropdown.value == "Day of Month (1st, 2nd, ect.)":
                        if day_of_month_dropdown.value is not None:
                            day_of_month_dropdown.border_color = None
                            date_to_save = day_of_month_dropdown.value
                            day_of_month_dropdown.update()
                        else:
                            day_of_month_dropdown.border_color = ft.colors.RED
                            day_of_month_dropdown.update()
                            return
                else:
                    day_of_week_or_month_dropdown.border_color = ft.colors.RED
                    day_of_week_or_month_dropdown.update()
                    return
        else:
            frequency_dropdown.border_color = ft.colors.RED
            frequency_dropdown.update()
            return
        if amount_due.value == "":
            amount_due.border_color = ft.colors.RED
            amount_due.update()
            return
        else:
            amount_due.border_color = None
            amount_due.update()
           
        json_data = {
            "user_id": user_id,
            "new_update": new_update,
            "due": date_to_save,
            "name": name_text.value,
            "amount": f"${amount_due.value}",
            "frequency": frequency_dropdown.value.lower(),
            "phone": phone_number.value,
            "website": website.value,
            "email": email.value,
        }
        error_text.visible = True
        page.update()
        print(json_data)
        response = add_update_bills(page, BASE_URL, json_data)
        if response == "success":
            page.go("/bills")
        else:
            error_text.value = "Something went wrong, please try again"
            error_text.visible = True
            page.update()

    if profile_pic:
        appbar = ft.AppBar(leading=ft.Row(controls=[ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=current_theme["top_appbar_colors"]["icon_color"], on_click=lambda _: page.go("/")),ft.Image(src=current_theme["top_appbar_colors"]["icon"], width=200, fit=ft.ImageFit.FIT_WIDTH)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"], actions=[ft.Container(content=ft.Image(src=profile_pic, width=40, height=40), border_radius=50, margin=ft.margin.only(right=10))])
    else:
        appbar = ft.AppBar(leading=ft.Row(controls=[ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=current_theme["top_appbar_colors"]["icon_color"], on_click=lambda _: page.go("/")),ft.Image(src=current_theme["top_appbar_colors"]["icon"], width=200, fit=ft.ImageFit.FIT_WIDTH)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"])
    floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=save, bgcolor=ft.colors.LIME_300)
    
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
                                floating_action_button=floating_action_button,
                                bgcolor=current_theme["background"]
                            )
                        )
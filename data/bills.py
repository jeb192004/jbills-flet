from flet import Page, dropdown
import httpx
import json

def get_bills(page: Page, user_id: str, BASE_URL: str):
        data = {"userId": user_id}  # Include user ID in the request data
        response = httpx.post(f"{BASE_URL}flet_login", json=data)
        if response.status_code == 200:
            try: 
                print("successfully fetched user and bills data") 
                user_bills_data = response.json()  
                user_data = user_bills_data['user']  
                if user_data == "no bills":
                    return {"error": "no bills"}
                else:
                    user_pay_hours = []
                    profile = user_data[0]
                    profile_pic = profile['image_url']
                    avg_pay = profile['avg_pay']
                    forty_hours = profile['forty_hour']
                    other_hours = profile['other_hours']
                    other_hours = json.loads(other_hours)
                    if forty_hours != None:
                         forty_hours = forty_hours.replace('$', '')
                         user_pay_hours.append(dropdown.Option(f"40 Hours: ${forty_hours}"),)
                    if avg_pay != None:
                         avg_pay = avg_pay.replace('$', '')
                         user_pay_hours.append(dropdown.Option(f"Average Pay: ${avg_pay}"),)
                    if other_hours != None:
                         if len(other_hours) > 0:
                              for pay_detail in other_hours:
                                   user_pay_hours.append(dropdown.Option(f"{pay_detail['hours']} Hours: {pay_detail['amount']}"),)
                        
                    my_bills = user_data[1]
                    unpaid_bills = user_data[2] if len(user_data) > 2 else []


                    return {"profile_pic": profile_pic, "user_pay_hours": user_pay_hours, "my_bills": my_bills, "unpaid_bills": unpaid_bills, "error": ""}
            except (KeyError, json.JSONDecodeError):
                # Handle error parsing the response
                print("Error: Invalid response from server")
        else:
            # Handle failed login attempt
            print(f"Error: {response.status_code}")

def save_unpaid_bills(page: Page, unpaid_bills, BASE_URL: str):
     response = httpx.post(f"{BASE_URL}add_unpaid", json={"unpaid": unpaid_bills})
     print(response.status_code)

def remove_unpaid_bills(page: Page, unpaid_bills, BASE_URL: str):         
     response = httpx.post(f"{BASE_URL}remove_past_due", json={"past_due": unpaid_bills})
     print(response)

def add_update_bills(page: Page, BASE_URL: str, data):
     
     response = httpx.post(f"{BASE_URL}data/add_bill", json=data)
     if response.status_code == 200:
          print(response)
          return "success"
     else:
          return "error"

def get_bills_object(data):
     try:
        pay_hours = []
        
            
        
            #print('Profile:\n', profile,)# '\nMy Bills:\n', my_bills, '\nUnpaid:\n', unpaid_bills)
            # Build the bills list
            #build_week_and_bills_list(page, my_bills, unpaid_bills)
                
     except Exception as e:
        print(f"Error fetching bills: {e}")

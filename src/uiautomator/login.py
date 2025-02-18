# left for easier debuging

# print(device.dump_hierarchy())  # Print all elements on the screen

# views = device(className="android.view.View") # List all instances of android.view.View
# for i, view in enumerate(views):
#     print(f"Instance {i}: {view.info}")

def Login(device, login, password):

    # click log in to get to the login prompts
    initial_login_button = device(className="android.view.View", instance=8)
    initial_login_button.click()

    # Wait until at least one EditText is visible (adjust timeout as needed)
    device(className="android.widget.EditText").wait(timeout=10)

    # put in email
    email_field = device(className="android.widget.EditText", instance=0)
    email_field.wait(timeout=10)
    email_field.click()
    email_field.set_text(login)
    device.press("back")

    # put in password
    password_field = device(className="android.widget.EditText", instance=1)
    password_field.wait(timeout=10)
    password_field.click()
    password_field.set_text(password)
    device.press("back")

    # click log in
    login_button = device(className="android.view.View", instance=7)  # the instance index changes if a wrong password is given
    login_button.wait(timeout=5)
    login_button.click()
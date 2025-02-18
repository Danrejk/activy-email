def Register(device, email, password, name, surname, nickname):

# 1st screen
    # click log in to get to the login prompts
    register_button = device(className="android.view.View", instance=6)
    register_button.click()

# 2nd screen
    # Wait until at least one EditText is visible (adjust timeout as needed)
    device(className="android.widget.EditText").wait(timeout=10)

    # put in email
    email_field = device(className="android.widget.EditText", instance=0)
    email_field.wait(timeout=10)
    email_field.click()
    email_field.set_text(email)
    device.press("back")

    # put in password
    password_field = device(className="android.widget.EditText", instance=1)
    password_field.wait(timeout=10)
    password_field.click()
    password_field.set_text(password)
    device.press("back")

    # put in password again
    password_field = device(className="android.widget.EditText", instance=2)
    password_field.wait(timeout=10)
    password_field.click()
    password_field.set_text(password)
    device.press("back")

    # click agree and register
    register_button = device(className="android.view.View", instance=16)
    register_button.wait(timeout=5)
    register_button.click()

# 3rd screen
    
### Here the avatar, name, surname and nickname will be put in. for now i'm not doing it to see how they will be handled

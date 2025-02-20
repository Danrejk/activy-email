from src.uiautomator.utils.waitForElement import waitForElement
from utils.clickNodeByClassInstance import clickNodeByClassInstance
from utils.setNodeTextByClassInstance import setNodeTextByClassInstance

def Register(device, email, password, name, surname, nickname):

# 1st screen
    # click log in to get to the login prompts
    lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 6)

# 2nd screen
    # Wait until at least one EditText is visible (adjust timeout as needed)
    device(className="android.widget.EditText").wait(timeout=50)
    # lastOnLastScreen.wait_gone(timeout=10) # this is buggy for some reason
    # put in email
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, email)
    # put in password
    setNodeTextByClassInstance(device, "android.widget.EditText", 1, password)
    # put in password again
    setNodeTextByClassInstance(device, "android.widget.EditText", 2, password)
    # click agree and register
    lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 16)

# 3rd screen
    lastOnLastScreen.wait_gone(timeout=10)
    # put name
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, name)
    # put surname
    setNodeTextByClassInstance(device, "android.widget.EditText", 1, surname)
    # put nickname
    setNodeTextByClassInstance(device, "android.widget.EditText", 2, nickname)
    # click next
    lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 13)

# 4th screen
    lastOnLastScreen.wait_gone(timeout=10)
    # select gender
    clickNodeByClassInstance(device, "android.widget.ImageView", 1)
    # click next
    lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 7)

# 5th screen
    lastOnLastScreen.wait_gone(timeout=25)

    # click next this one is way different than the rest, due to the fact that the developers of Activy made it a very weird hierarchy node
    # this is clicked too early
    main_view = waitForElement(device, className="android.view.View", instance=0)
    if main_view.exists:
        bounds = main_view.info['bounds']
        center_x = (bounds['left'] + bounds['right']) // 2
        bottom_y = bounds['bottom'] - 80
        device.click(center_x, bottom_y)
    else:
        raise ValueError("Main view not found")

# 6th screen
    main_view.wait_gone(timeout=10)
    # type 88
    device.send_keys(text='88')
    # click next
    lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 7)

# 7th screen
    lastOnLastScreen.wait_gone(timeout=10)
    # click next
    lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 7)

# 8th screen
    lastOnLastScreen.wait_gone(timeout=10)
    # click agree
    lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 11)

# 9th screen
    lastOnLastScreen.wait_gone(timeout=10)
    # click next
    lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 11)

# 10th screen
    lastOnLastScreen.wait_gone(timeout=10)
    # click next
    lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 11)

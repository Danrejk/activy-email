from utils.clickNodeByClassInstance import clickNodeByClassInstance
from utils.setNodeTextByClassInstance import setNodeTextByClassInstance

def Register(device, email, password, name, surname, nickname):

# 1st screen
    # click log in to get to the login prompts
    lastOn1stScreen = clickNodeByClassInstance(device, "android.view.View", 6)

# 2nd screen
    # Wait until at least one EditText is visible (adjust timeout as needed)
    device(className="android.widget.EditText").wait(timeout=10)
    # lastOn1stScreen.wait_gone(timeout=10) # this is buggy for some reason

    # put in email
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, email)

    # put in password
    setNodeTextByClassInstance(device, "android.widget.EditText", 1, password)

    # put in password again
    setNodeTextByClassInstance(device, "android.widget.EditText", 2, password)

    # click agree and register
    lastOn2ndScreen = clickNodeByClassInstance(device, "android.view.View", 16)

# 3rd screen
    device(className="android.widget.EditText").wait(timeout=1)
    lastOn2ndScreen.wait_gone(timeout=10)

    # put name
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, name)

    # put surname
    setNodeTextByClassInstance(device, "android.widget.EditText", 1, surname)

    # put nickname
    setNodeTextByClassInstance(device, "android.widget.EditText", 2, nickname)

    # click next
    clickNodeByClassInstance(device, "android.view.View", 13)
    
# 4th screen


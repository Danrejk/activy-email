from utils.clickNodeByClassInstance import clickNodeByClassInstance
from utils.setNodeTextByClassInstance import setNodeTextByClassInstance

def Login(device, email, password):
    # click log in to get to the login prompts
    clickNodeByClassInstance(device, "android.view.View", 8)

    # Wait until at least one EditText is visible (adjust timeout as needed)
    device(className="android.widget.EditText").wait(timeout=10)

    # put in email
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, email)

    # put in password
    setNodeTextByClassInstance(device, "android.widget.EditText", 1, password)

    # click log in
    clickNodeByClassInstance(device, "android.view.View", 7, 2)

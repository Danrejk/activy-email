from utils.clickNodeByClassInstance import clickNodeByClassInstance
from utils.setNodeTextByClassInstance import setNodeTextByClassInstance

def Register(device, email, password, name, surname, nickname):

# # 1st screen
#     # click log in to get to the login prompts
#     lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 6)
#
# # 2nd screen
#     # Wait until at least one EditText is visible (adjust timeout as needed)
#     device(className="android.widget.EditText").wait(timeout=10)
#     # lastOnLastScreen.wait_gone(timeout=10) # this is buggy for some reason
#
#     # put in email
#     setNodeTextByClassInstance(device, "android.widget.EditText", 0, email)
#
#     # put in password
#     setNodeTextByClassInstance(device, "android.widget.EditText", 1, password)
#
#     # put in password again
#     setNodeTextByClassInstance(device, "android.widget.EditText", 2, password)
#
#     # click agree and register
#     lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 16)
#
# # 3rd screen
#     lastOnLastScreen.wait_gone(timeout=10)
#
#     # put name
#     setNodeTextByClassInstance(device, "android.widget.EditText", 0, name)
#
#     # put surname
#     setNodeTextByClassInstance(device, "android.widget.EditText", 1, surname)
#
#     # put nickname
#     setNodeTextByClassInstance(device, "android.widget.EditText", 2, nickname)
#
#     # click next
#     lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 13)
#
# # 4th screen
#     lastOnLastScreen.wait_gone(timeout=10)
#
#     # select gender
#     clickNodeByClassInstance(device, "android.widget.ImageView", 1)
#
#     # click next
#     lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 7)
#
# # 5th screen
#     lastOnLastScreen.wait_gone(timeout=10)

    # click next
    lastOnLastScreen = clickNodeByClassInstance(device, "android.view.View", 6, child=1)

from src.activy.utils.getStage import load_templates
from src.activy.utils.checkStage import tryCheckStage
from src.activy.utils.controlNodes.clickNodeByClassInstance import clickNodeByClassInstance

def logoutStage1(device, templates):
    """
    Stage 1: Click the settings
    """
    # this has to be done with proportions to click in a specific area where the tab selector is
    # the challange button is an imageView which has a varries ammount of instances
    width = device.info["displayWidth"]
    height = device.info["displayHeight"]
    x = int(width * 12 / 13)
    y = int(100)
    device.click(x, y)

    try:
        tryCheckStage(device, "mainMenu", templates)
        raise ValueError("Didn't move to settings.")
    except:
        print("Stage 1 completed")

def logoutStage2(device, templates):
    """
    Stage 2: Click the logout button
    """
    device(scrollable=True).scroll.vert.toEnd()
    clickNodeByClassInstance(device, "android.widget.Button", 0)

    tryCheckStage(device, "login", templates)
    print("Stage 2 completed")

def Logout(device):
    templates = load_templates("opencv/generalNavigation")

    logoutStage1(device, templates)
    logoutStage2(device, templates)

    print("Logged out")

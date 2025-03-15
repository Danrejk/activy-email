from src.activy.utils.clickSettings import clickSettings
from src.activy.utils.stage.checkStage import tryCheckStage
from src.activy.utils.controlNodes.clickNodeByClassInstance import clickNodeByClassInstance
from src.activy.utils.stage.loadTemplates import load_templates


def logoutStage1(device, templates):
    """
    Stage 1: Click the settings
    """
    clickSettings(device)

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

from src.activy.utils.clickSettings import clickSettings
from src.activy.utils.controlNodes.waitForElement import waitForElement
from src.activy.utils.stage.getStage import load_templates, getStage
from src.activy.utils.stage.checkStage import tryCheckStage
from src.activy.utils.controlNodes.clickNodeByClassInstance import clickNodeByClassInstance
from src.activy.utils.controlNodes.setNodeTextByClassInstance import setNodeTextByClassInstance

def connectStravaStage1(device, templates):
    """
    Stage 1: Click the settings
    """
    clickSettings(device)

    try:
        tryCheckStage(device, "mainMenu", templates)
        raise ValueError("Didn't move to settings.")
    except:
        print("Stage 1 completed")

def connectStravaStage2(device, templates):
    """
    Stage 2: Click app integrations.

    Failsafe: It stops if it detects 2f001 (Strava already connected)
    """
    clickNodeByClassInstance(device, "android.view.View", 8)

    try:
        tryCheckStage(device, 2, templates)
    except ValueError as e:
        if getStage(device, templates)[0] == "2f001":
            print("Strava already connected")
        raise e

    print("Stage 2 completed")

def connectStravaStage3(device, templates):
    """
    Stage 3: Select Strava.
    """
    clickNodeByClassInstance(device, "android.view.View", 8)

    tryCheckStage(device, 3, templates)
    print("Stage 3 completed")

def connectStravaStage4(device, templates):
    """
    Stage 4: Click connect with Strava.
    """

    # This has to be done using child of view4 because it's an imageView and those have a changing index
    parent_view = waitForElement(device, className="android.view.View", instance=4)
    if parent_view.exists:
        child_view = parent_view.child(index=4)
        if child_view.exists:
            child_view.click()
        else:
            raise ValueError("Connect with Strava button not found")
    else:
        raise TimeoutError("Didn't find the parent view")

    try:
        stage = tryCheckStage(device, ["4","4o401","401or4o402","402or4o403"], templates, retries=50)
        if stage[0] == "4o401":
            connectStravaStage401(device, templates)
        elif stage[0] == "401or4o402":
            connectStravaStage402(device, templates)
        elif stage[0] == "402or4o403":
            connectStravaStage403(device, templates)

    except:
        raise TimeoutError("Connect with Strava button not found or didn't properly move to the login screen")

    print("Stage 4 completed")

# 401, 402, 403 are only neccessary if it's the first time
def connectStravaStage401(device, templates):
    """
    Stage 401: Accept chrome statistics on first launch
    (Sometimes it can be skipped and go straight to 402)
    """
    clickNodeByClassInstance(device, "android.widget.Button", 0)

    try:
        stage = tryCheckStage(device, ["4", "401or4o402","402or4o403"], templates)
        if stage[0] == "401or4o402":
            connectStravaStage402(device, templates)
        elif stage[0] == "402or4o403":
            connectStravaStage403(device, templates)
    except:
        raise TimeoutError("Didn't accept chrome statistics or didn't properly move to the login screen")

    print("Stage 401 completed")

def connectStravaStage402(device, templates):
    """
    Stage 402: Decline synchronisation
    """
    clickNodeByClassInstance(device, "android.widget.Button", 0)

    try:
        stage = tryCheckStage(device, ["4", "402or4o403"], templates)
        if stage[0] == "402or4o403":
            connectStravaStage403(device, templates)
    except:
        raise TimeoutError("Didn't decline synchronisation or didn't properly move to the login screen")
    print("Stage 402 completed")

def connectStravaStage403(device, templates):
    """
    Stage 403: Accept cookies
    """
    clickNodeByClassInstance(device, "android.widget.Button", 0)

    tryCheckStage(device, 4, templates)
    print("Stage 403 completed")

def connectStravaStage5(device, templates, email):
    """
    Stage 5: Put in email.
    """
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, email)
    clickNodeByClassInstance(device, "android.widget.Button", 5)

    tryCheckStage(device, 5, templates)
    print("Stage 5 completed")

def connectStravaStage6(device, templates, password):
    """
    Stage 6: Put in password.
    """
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, password)
    clickNodeByClassInstance(device, "android.widget.Button", 3)

    tryCheckStage(device, 6, templates)
    print("Stage 6 completed")

def connectStravaStage7(device, templates):
    """
    Stage 7: Authorise Activy.
    """
    clickNodeByClassInstance(device, "android.widget.Button", 0)

    tryCheckStage(device, 7, templates)
    print("Stage 7 completed")

def connectStravaStage8(device, templates):
    """
    Stage 8: Go back to main screen.
    """
    device.press("back")
    device.press("back")
    device.press("back")

    tryCheckStage(device, 8, templates)
    print("Stage 8 completed")


def connectStrava(device, email, password):
    templates = load_templates("opencv/connectStrava")
    templatesGeneralNavigation = load_templates("opencv/generalNavigation")

    connectStravaStage1(device, templatesGeneralNavigation)
    connectStravaStage2(device, templates)
    connectStravaStage3(device, templates)

    # PROBLEM. The user is still logged onto strava
    # try:
    #     clearChrome()
    # except ValueError as e:
    #     raise e

    connectStravaStage4(device, templates)
    connectStravaStage5(device, templates, email)
    connectStravaStage6(device, templates, password)
    connectStravaStage7(device, templates)
    connectStravaStage8(device, templates)

    print(f"Connected strava for {email}")



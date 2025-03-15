import time

from src.activy.utils.clickSettings import clickSettings
from src.activy.utils.controlNodes.waitForElement import waitForElement
from src.activy.utils.stage.getStage import getStage
from src.activy.utils.stage.checkStage import tryCheckStage
from src.activy.utils.controlNodes.clickNodeByClassInstance import clickNodeByClassInstance
from src.activy.utils.controlNodes.setNodeTextByClassInstance import setNodeTextByClassInstance
from src.activy.utils.stage.loadTemplates import load_templates


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
        stage = tryCheckStage(device, ["4", "4o401", "401or4o402", "402or4o403"], templates, retries=50)
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
        stage = tryCheckStage(device, ["4", "401or4o402", "402or4o403"], templates)
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
    Branching: 501 Sometimes Strava will promt you to switch to one-time codes, reject it
    """
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, email)
    clickNodeByClassInstance(device, "android.widget.Button", 5)

    try:
        stage = tryCheckStage(device, [5,"5o501"], templates, ignored_stage="4")
        if stage == "5o501":
            connectStravaStage501(device, templates)
    except ValueError as e:
        raise e
    print("Stage 5 completed")


def connectStravaStage501(device, templates):
    """
    Stage 501: Reject one-time codes by clicking 'Use password instead'
    """

    # unfortunately hardcoded due to the lack of a proper way to identify the button
    # if this proves to be a problem in the future, we can use opencv to find the location of the button

    device.swipe(360, 600, 360, 200, 0.1)
    # these clicks are done in this way to trick recaptcha
    device.long_click(350, 900, 0.5)
    device.long_click(350.1, 912.2, 0.1)
    device.swipe(360, 400, 360, 800, 0.1)

    tryCheckStage(device, 5, templates, ignored_stage=4)
    print("Stage 501 completed")


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
    time.sleep(0.2)
    device.press("back")
    time.sleep(0.2)
    device.press("back")
    time.sleep(0.2)
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

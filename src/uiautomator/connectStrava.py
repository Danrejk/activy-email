from src.opencv.getStage import load_templates, getStage
from src.uiautomator.utils.checkStage import tryCheckStage
from src.uiautomator.utils.controlNodes.clickNodeByClassInstance import clickNodeByClassInstance
from src.uiautomator.utils.controlNodes.setNodeTextByClassInstance import setNodeTextByClassInstance

def connectStravaStage1(device, templates):
    """
    Stage 1: Click the settings button.
    """
    clickNodeByClassInstance(device, "android.widget.ImageView", 2)

    tryCheckStage(device, 1, templates, retries=5)
    print("Stage 1 completed")

def connectStravaStage2(device, templates):
    """
    Stage 2: Click app integrations.
    """
    clickNodeByClassInstance(device, "android.view.View", 8)

    try:
        tryCheckStage(device, 2, templates, retries=5)
    except ValueError as e:
        if getStage(device, templates)[0] == 200:
            print("Strava already connected")
        raise e

    print("Stage 2 completed")

def connectStravaStage3(device, templates):
    """
    Stage 3: Select Strava.
    """
    clickNodeByClassInstance(device, "android.view.View", 8)

    tryCheckStage(device, 3, templates, retries=5)
    print("Stage 3 completed")

def connectStravaStage4(device, templates):
    """
    Stage 4: Click connect with Strava.
    """
    clickNodeByClassInstance(device, "android.widget.ImageView", 4)

    try:
        tryCheckStage(device, 4, templates, retries=75)
    except:
        try:
            tryCheckStage(device, 400, templates, retries=5)
            connectStravaStage400(device, templates)
        except:
            tryCheckStage(device, 401, templates, retries=5)
            connectStravaStage401(device, templates)

    print("Stage 4 completed")

# 400, 401, 402 are only neccessary if it's the first time
def connectStravaStage400(device, templates):
    """
    Stage 400: Accept chrome statistics on first launch
    """
    clickNodeByClassInstance(device, "android.widget.Button", 0)

    try:
        tryCheckStage(device, 401, templates, retries=5)
        connectStravaStage401(device, templates)
    except:
        tryCheckStage(device, 4, templates, retries=5)

    print("Stage 400 completed")

def connectStravaStage401(device, templates):
    """
    Stage 401: Decline synchronisation
    """
    clickNodeByClassInstance(device, "android.widget.Button", 0)

    try:
        tryCheckStage(device, 402, templates, retries=5)
        connectStravaStage401(device, templates)
    except:
        tryCheckStage(device, 4, templates, retries=5)
    print("Stage 401 completed")

def connectStravaStage402(device, templates):
    """
    Stage 402: Accept cookies
    """
    clickNodeByClassInstance(device, "android.widget.Button", 0)

    tryCheckStage(device, 4, templates, retries=5)
    print("Stage 402 completed")

def connectStravaStage5(device, templates, email):
    """
    Stage 5: Put in email.
    """
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, email)
    clickNodeByClassInstance(device, "android.widget.Button", 5)

    tryCheckStage(device, 5, templates, retries=10) # more retries due to an object from stage 4 still being present
    print("Stage 5 completed")

def connectStravaStage6(device, templates, password):
    """
    Stage 6: Put in password.
    """
    # to be tested
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, password)
    clickNodeByClassInstance(device, "android.widget.Button", 3)

    tryCheckStage(device, 6, templates, retries=5)
    print("Stage 6 completed")

def connectStravaStage7(device, templates):
    """
    Stage 7: Authorise Activy.
    """
    clickNodeByClassInstance(device, "android.widget.Button", 0)

    tryCheckStage(device, 7, templates, retries=5)
    print("Stage 7 completed")

def connectStravaStage8(device, templates):
    """
    Stage 8: Go back to main screen.
    """
    device.press("back")
    device.press("back")
    device.press("back")

    tryCheckStage(device, 8, templates, retries=5)
    print("Stage 8 completed")


def connectStrava(device, email, password):
    templates = load_templates("../opencv/connectStrava")

    connectStravaStage1(device, templates)
    connectStravaStage2(device, templates)
    connectStravaStage3(device, templates)
    connectStravaStage4(device, templates)
    # PROBLEM. The user is still logged onto strava
    connectStravaStage5(device, templates, email)
    connectStravaStage6(device, templates, password)
    connectStravaStage7(device, templates)
    connectStravaStage8(device, templates)

    print(f"Connected strava for {email}")



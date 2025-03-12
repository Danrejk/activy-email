import time

from src.activy.utils.getStage import load_templates
from src.activy.utils.checkStage import tryCheckStage
from src.activy.utils.checkStage import checkStage
from src.activy.utils.controlNodes.clickNodeByClassInstance import clickNodeByClassInstance
import re

def pointsStage1(device, templates, challangeName):
    """
    Stage 1: Click the challanges button.

    Branching: if there is no challange selected - it goes to 101
    """
    # this has to be done with proportions to click in a specific area where the tab selector is
    # the challange button is an imageView which has a varries ammount of instances
    width = device.info["displayWidth"]
    height = device.info["displayHeight"]
    x = int(width * 5 / 6)
    y = int(height - 10)
    device.click(x, y)

    stage = None
    for i in range(20):
        try:
            stage = checkStage(device, "1o101", templates)[0]
            pointsStage101(device, templates, challangeName)
            break
        except:
            if device(descriptionContains=challangeName):
                stage = "1o2"
                break
        time.sleep(0.5)

    print(stage)
    if stage is None:
        raise ValueError("Failed to select a challange after 10s")
    else:
        print("Stage 1 completed")

        if stage == "1o101":
            pointsStage101(device, templates, challangeName)
        elif stage == "1o2":
            print("Skipping stage 1o101 and 1o102")

def pointsStage101(device, template, challangeName):
    """
    Stage 101: Click select challange
    """
    clickNodeByClassInstance(device, "android.view.View", 5)

    for i in range(10):
        if device(descriptionContains=challangeName):
            print("Stage 101 completed")
            pointsStage102(device, template, challangeName)
            break
        time.sleep(1)

def pointsStage102(device, templates, challangeName):
    """
    Stage 102: Select challange to check
    """
    device(descriptionContains=challangeName).click()
    device(descriptionContains=challangeName).wait_gone(timeout=10)
    clickNodeByClassInstance(device, "android.view.View", 6)

    # check if the correct one got selected
    for i in range(10):
        view = device(className="android.view.View", instance=7)
        if view.exists and challangeName in view.info.get("contentDescription", ""):
            print("Stage 102 completed")
            return

        time.sleep(0.5)  # Wait 0.5s before retrying

    raise TimeoutError("Didn't move to the challange screen within 5 seconds.")

def pointsStage2(device, templates):
    """
    Stage 2: Check user's points
    """
    visiblePoints = []  # this is only the points up to the user's point since there is no point in recording all of them

    for i in range(20):
        image_views = device(className="android.widget.ImageView", descriptionContains="pkt")
        if image_views:
            for view in image_views:
                desc = view.info["contentDescription"]
                match = re.search(r"(\d+)\s*pkt", desc)
                if match:
                    visiblePoints.append(match.group(1))
                if len(visiblePoints) > 1:
                    print("Stage 4 completed")
                    return visiblePoints[1]  # the user's points are always listed second
        time.sleep(0.5)

    raise TimeoutError("Didn't find user's points within 10s")

def pointsStage3(device, templates):
    """
    Stage 3: Go back to main screen
    """
    # this has to be done with proportions to click in a specific area where the tab selector is
    # the challange button is an imageView which has a varries ammount of instances
    width = device.info["displayWidth"]
    height = device.info["displayHeight"]
    x = int(width * 1 / 6)
    y = int(height - 10)
    device.click(x, y)

    tryCheckStage(device, "mainMenu", templates)


def checkPoints(device, challangeName):
    templates = load_templates("opencv/checkPoints")
    templatesStage3 = load_templates("opencv/generalNavigation")

    pointsStage1(device, templates, challangeName)
    userPoints = pointsStage2(device, templates)
    pointsStage3(device, templatesStage3)

    print("Checked points")
    return userPoints

import time

from src.opencv.getStage import load_templates
from src.uiautomator.utils.checkStage import tryCheckStage
from src.uiautomator.utils.controlNodes.clickNodeByClassInstance import clickNodeByClassInstance
from src.uiautomator.utils.controlNodes.setNodeTextByClassInstance import setNodeTextByClassInstance
import re


def pointsStage1(device, templates):
    """
    Stage 1: Click the challanges button.
    """

    # this has to be done with proportions to click in a specific area where the tab selector is
    # the challange button is an imageView which has a varries ammount of instances
    width = device.info["displayWidth"]
    height = device.info["displayHeight"]
    x = int(width * 5 / 6)
    y = int(height - 10)
    device.click(x, y)

    # TODO
    # device(className="android.widget.EditText").wait(timeout=10)
    print("Stage 1 completed")


def pointsStage2(device, templates, challangeName):
    """
    Stage 2: Select challange to check
    """
    device(descriptionContains=challangeName).click()

    start_time = time.time()
    while time.time() - start_time < 5:
        view = device(className="android.view.View", instance=7)
        if view.exists and challangeName in view.info.get("contentDescription", ""):
            print("Stage 2 completed")
            return

        time.sleep(0.5)  # Wait 0.5s before retrying

    raise TimeoutError("Didn't move to the challange screen within 5 seconds.")

def pointsStage3(device, templates):
    image_views = device(className="android.widget.ImageView", descriptionContains="pkt")

    visiblePoints = []  # this is only the points up to the user's point since there is no point in recording all of them
    userPoints = 0

    for view in image_views:
        desc = view.info["contentDescription"]
        match = re.search(r"(\d+)\s*pkt", desc)
        if match:
            visiblePoints.append(match.group(1))
        if len(visiblePoints) > 1:
            userPoints = visiblePoints[1]  # the user's points are always listed second

    print("Stage 3 completed")
    return userPoints


def checkPoints(device, challangeName):
    templates = load_templates("../opencv/checkPoints")

    pointsStage1(device, templates)
    pointsStage2(device, templates, challangeName)
    userPoints = pointsStage3(device, templates)

    print("checked points")
    return userPoints

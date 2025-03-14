from time import sleep

from src.activy.utils.stage.getStage import load_templates
from src.activy.utils.stage.checkStage import tryCheckStage
from src.activy.utils.controlNodes.clickNodeByClassInstance import clickNodeByClassInstance
from src.activy.utils.getCurretlyOpenApp import getCurrentlyOpenApp

def updateStage1(device, templates):
    """
    Stage 1: Check if an update is needed

    Branching: If an update is needed, 101 is initiated
    """
    try:
        tryCheckStage(device, "1o101", templates)
        print("Stage 1 completed")
        updateStage101(device, templates)
    except:
        print("App is up to date!")


# The below stages apply only if an update is needed
def updateStage101(device, templates):
    """
    Stage 101: Click on "Update" button to go to Google Play
    """
    clickNodeByClassInstance(device, "android.view.View", 6)

    tryCheckStage(device, 101, templates)
    print("Stage 101 completed")
    updateStage102(device, templates)

def updateStage102(device, templates):
    """
    Stage 102: Click on "Update" button in Google Play and wait for it to finsih downloading
    """
    clickNodeByClassInstance(device, "android.widget.Button", 1)
    sleep(2)  # not sure if this is needed, but it's so that the update has time to start after being clicked

    # this waits for the Update/Open button to become clickable again, since it's not clickable during the updating process
    for i in range(100):
        button_node = device(className="android.widget.Button", instance=1)
        parent_node = button_node.xpath("..")  # get the parent view which is actually clickable

        if parent_node.exists and parent_node.info.get("enabled") is True:
            print("Stage 102 completed")
            updateStage103(device, templates)
            return
        sleep(1)

    print("Failed to update the app within 100s")


def updateStage103(device, templates):
    """
        Stage 103: Click the "Open" button to go back to Activy
    """
    clickNodeByClassInstance(device, "android.widget.Button", 1)

    for i in range(50):
        current_package = getCurrentlyOpenApp(device)

        if current_package == "com.activy":
            print("Stage 103 completed")
            sleep(5)  # wait 5s to let the UI load
            print("Succesfully Updated!")
            return

        sleep(1)

    print("Failed to open Activy within 50s")


def UpdateApp(device):
    templates = load_templates("opencv/appUpdate")

    updateStage1(device, templates)


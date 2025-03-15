import subprocess
import time

from src.activy.utils.getControl import getControl
from src.activy.utils.getCurretlyOpenApp import getCurrentlyOpenApp
from src.activy.utils.isAdbAvailable import isAdbAvailable
from src.activy.utils.stage.checkStage import tryCheckStage
from src.activy.utils.controlNodes.waitForElement import waitForElement
from src.activy.utils.controlNodes.clickNodeByClassInstance import clickNodeByClassInstance
from src.activy.utils.controlNodes.setNodeTextByClassInstance import setNodeTextByClassInstance
from src.activy.utils.stage.loadTemplates import load_templates


def registerStage1(device, templates):
    """
    Stage 1: Click the register button.
    """
    clickNodeByClassInstance(device, "android.view.View", 6)

    tryCheckStage(device, 1, templates)
    print("Stage 1 completed")

def registerStage2(device, templates, email, password):
    """
    Stage 2: Enter email and password.
    """
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, email)
    setNodeTextByClassInstance(device, "android.widget.EditText", 1, password)
    setNodeTextByClassInstance(device, "android.widget.EditText", 2, password)
    clickNodeByClassInstance(device, "android.view.View", 16)

    tryCheckStage(device, 2, templates)
    print("Stage 2 completed")

def registerStage3(device, templates, controlsTemplates, name, surname, nickname, avatar=None):
    """
    Stage 3: Enter name, surname, and nickname.
    """
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, name)
    setNodeTextByClassInstance(device, "android.widget.EditText", 1, surname)
    setNodeTextByClassInstance(device, "android.widget.EditText", 2, nickname)

    # Avatar selection
    if avatar:
        coordinates = getControl(device, templates, "addAvatar", debug=True)
        device.click(coordinates[0], coordinates[1])
        clickNodeByClassInstance(device, "android.view.View", 5)
        for i in range (0, 10):
            if getCurrentlyOpenApp(device) == "com.google.android.documentsui":
                registerStage301(device, templates, controlsTemplates, avatar)
                break
            if i == 9:
                raise ValueError("Didn't move to gallery app")
            time.sleep(1)

    clickNodeByClassInstance(device, "android.view.View", 13)

    tryCheckStage(device, 3, templates)
    print("Stage 3 completed")

def registerStage301(device, templates, controlsTemplates, avatarPath):
    """
    Stage 301: Send image to AVD and select image in gallery.
    """
    if not isAdbAvailable():
        raise EnvironmentError("ADB is not available in PATH. Please install ADB and add it to your system PATH.")

    # send image to avd
    avdAvatarPath = "/sdcard/Download/avatar.png"
    adbPushCommand = f"adb push \"{avatarPath}\" \"{avdAvatarPath}\""
    result = subprocess.run(adbPushCommand, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to push avatar to AVD: {result.stderr}")

    # navigate through gallery
    clickNodeByClassInstance(device, "android.widget.ImageButton", 0)
    templates = load_templates("opencv/register/controls")
    time.sleep(0.75)
    coordinates = getControl(device, templates, "downloads", debug=True)
    device.click(coordinates[0], coordinates[1])

    try:
        avatar_element = waitForElement(device, contentDesc="avatar.png, ")
        avatar_element.click()
    except Exception as e:
        print(f"Failed to find avatar.png: {e}")

    time.sleep(1)
    clickNodeByClassInstance(device, "android.widget.Button", 0)

    try:
        tryCheckStage(device, 2, templates)
        print("Stage 301 completed")
    except Exception as e:
        raise TimeoutError(f"Failed to select an Avatar: {e}")


def registerStage4(device, templates):
    """
    Stage 4: Select gender and click next.
    """

    # this has to be done using child of view6 because it's an imageView and those have a changing index
    parent_view = waitForElement(device, className="android.view.View", instance=6)
    if parent_view.exists:
        child_view = parent_view.child(index=0)
        if child_view.exists:
            child_view.click()
        else:
            raise ValueError("Gender button not found")
    else:
        raise ValueError("Gender button array view not found")

    clickNodeByClassInstance(device, "android.view.View", 7)

    tryCheckStage(device, 4, templates)
    print("Stage 4 completed")

def registerStage5(device, templates):
    """
    Stage 5: Click next.
    """
    main_view = waitForElement(device, className="android.view.View", instance=0)
    if main_view.exists:
        bounds = main_view.info['bounds']
        center_x = (bounds['left'] + bounds['right']) // 2
        bottom_y = bounds['bottom'] - 80
        device.click(center_x, bottom_y)
    else:
        raise ValueError("Main view not found")
    tryCheckStage(device, 5, templates)
    print("Stage 5 completed")

def registerStage6(device, templates):
    """
    Stage 6: Enter weight 88 and click next.
    """
    device.send_keys(text='88')
    clickNodeByClassInstance(device, "android.view.View", 7)

    tryCheckStage(device, 6, templates)
    print("Stage 6 completed")

def registerStage7(device, templates):
    """
    Stage 7: Click next.
    """
    clickNodeByClassInstance(device, "android.view.View", 7)

    tryCheckStage(device, 7, templates)
    print("Stage 7 completed")

def registerStage8(device, templates):
    """
    Stage 8: Click agree.
    """
    clickNodeByClassInstance(device, "android.view.View", 11)

    tryCheckStage(device, 8, templates)
    print("Stage 8 completed")

def registerStage9(device, templates):
    """
    Stage 9: Click next.
    """
    last_node = clickNodeByClassInstance(device, "android.view.View", 11)
    last_node.wait_gone(timeout=50)
    print("Stage 9 completed")

# HERE THERE HAVE TO BE MORE STAGES FOR SELECTING CHALLENGES


def register(device, email, password, name, surname, nickname, avatar=None):
    templates = load_templates("opencv/register")
    controlsTemplates = load_templates("opencv/register/controls")

    # registerStage1(device, templates)
    # registerStage2(device, templates, email, password)
    registerStage3(device, templates, controlsTemplates,  name, surname, nickname, avatar)
    # registerStage4(device, templates)
    # registerStage5(device, templates)
    # registerStage6(device, templates)
    # registerStage7(device, templates)
    # registerStage8(device, templates)
    # registerStage9(device, templates)

    print(f"Registered {nickname}")

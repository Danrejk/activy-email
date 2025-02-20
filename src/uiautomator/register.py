from src.uiautomator.utils.waitForElement import waitForElement
from utils.clickNodeByClassInstance import clickNodeByClassInstance
from utils.setNodeTextByClassInstance import setNodeTextByClassInstance

def registerStage1(device):
    """
    Stage 1: Click the register button.
    """
    last_node = clickNodeByClassInstance(device, "android.view.View", 6)
    last_node.wait_gone(timeout=10)
    # Wait until at least one EditText is visible
    device(className="android.widget.EditText").wait(timeout=50)
    return

def registerStage2(device, email, password):
    """
    Stage 2: Enter email and password.
    """
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, email)
    setNodeTextByClassInstance(device, "android.widget.EditText", 1, password)
    setNodeTextByClassInstance(device, "android.widget.EditText", 2, password)
    last_node = clickNodeByClassInstance(device, "android.view.View", 16)
    last_node.wait_gone(timeout=10)
    return

def registerStage3(device, name, surname, nickname):
    """
    Stage 3: Enter name, surname, and nickname.
    """
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, name)
    setNodeTextByClassInstance(device, "android.widget.EditText", 1, surname)
    setNodeTextByClassInstance(device, "android.widget.EditText", 2, nickname)
    last_node = clickNodeByClassInstance(device, "android.view.View", 13)
    last_node.wait_gone(timeout=10)
    return

def registerStage4(device):
    """
    Stage 4: Select gender and click next.
    """
    clickNodeByClassInstance(device, "android.widget.ImageView", 1)  # select gender
    last_node = clickNodeByClassInstance(device, "android.view.View", 7)  # click next
    last_node.wait_gone(timeout=10)
    return

def registerStage5(device):
    """
    Stage 5: Click next.
    """
    # this one is way different than the rest, due to the fact that the developers of Activy made it a very weird hierarchy node
    main_view = waitForElement(device, className="android.view.View", instance=0)
    if main_view.exists:
        bounds = main_view.info['bounds']
        center_x = (bounds['left'] + bounds['right']) // 2
        bottom_y = bounds['bottom'] - 80
        device.click(center_x, bottom_y)
    else:
        raise ValueError("Main view not found")
    main_view.wait_gone(timeout=10)
    return

def registerStage6(device):
    """
    Stage 6: Enter weight 88 and click next.
    """
    device.send_keys(text='88')
    last_node = clickNodeByClassInstance(device, "android.view.View", 7)
    last_node.wait_gone(timeout=10)
    return

def registerStage7(device):
    """
    Stage 7: Click next.
    """
    last_node = clickNodeByClassInstance(device, "android.view.View", 7)
    last_node.wait_gone(timeout=10)
    return

def registerStage8(device):
    """
    Stage 8: Click agree.
    """
    last_node = clickNodeByClassInstance(device, "android.view.View", 11)
    last_node.wait_gone(timeout=10)
    return

def registerStage9(device):
    """
    Stage 9: Click next.
    """
    last_node = clickNodeByClassInstance(device, "android.view.View", 11)
    last_node.wait_gone(timeout=10)
    return

def registerStage10(device):
    """
    Stage 10: Click next.
    """
    last_node = clickNodeByClassInstance(device, "android.view.View", 11)
    last_node.wait_gone(timeout=10)
    return

def Register(device, email, password, name, surname, nickname):
    registerStage1(device)
    registerStage2(device, email, password)
    registerStage3(device, name, surname, nickname)
    registerStage4(device)
    registerStage5(device)
    registerStage6(device)
    registerStage7(device)
    registerStage8(device)
    registerStage9(device)
    registerStage10(device)

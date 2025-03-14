from src.activy.utils.stage.getStage import load_templates
from src.activy.utils.stage.checkStage import tryCheckStage
from src.activy.utils.controlNodes.waitForElement import waitForElement
from src.activy.utils.controlNodes.clickNodeByClassInstance import clickNodeByClassInstance
from src.activy.utils.controlNodes.setNodeTextByClassInstance import setNodeTextByClassInstance

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

def registerStage3(device, templates, name, surname, nickname):
    """
    Stage 3: Enter name, surname, and nickname.
    """
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, name)
    setNodeTextByClassInstance(device, "android.widget.EditText", 1, surname)
    setNodeTextByClassInstance(device, "android.widget.EditText", 2, nickname)
    clickNodeByClassInstance(device, "android.view.View", 13)

    tryCheckStage(device, 3, templates)
    print("Stage 3 completed")

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


def Register(device, email, password, name, surname, nickname):
    templates = load_templates("opencv/register")

    registerStage1(device, templates)
    registerStage2(device, templates, email, password)
    registerStage3(device, templates, name, surname, nickname)
    registerStage4(device, templates)
    registerStage5(device, templates)
    registerStage6(device, templates)
    registerStage7(device, templates)
    registerStage8(device, templates)
    registerStage9(device, templates)

    print(f"Registered {nickname}")

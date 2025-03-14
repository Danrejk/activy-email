from src.activy.utils.stage.getStage import load_templates
from src.activy.utils.stage.checkStage import tryCheckStage
from src.activy.utils.controlNodes.clickNodeByClassInstance import clickNodeByClassInstance
from src.activy.utils.controlNodes.setNodeTextByClassInstance import setNodeTextByClassInstance

def loginStage1(device, templates):
    """
    Stage 1: Click the login button.
    """
    clickNodeByClassInstance(device, "android.view.View", 8)

    device(className="android.widget.EditText").wait(timeout=10)
    print("Stage 1 completed")

def loginStage2(device, templates, email, password):
    """
    Stage 2: Put in credentials and log in.
    """
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, email)
    setNodeTextByClassInstance(device, "android.widget.EditText", 1, password)
    clickNodeByClassInstance(device, "android.view.View", 7)

    tryCheckStage(device, "mainMenu", templates, retries=50)
    print("Stage 2 completed")

def Login(device, email, password):
    templates = load_templates("opencv/generalNavigation")

    loginStage1(device, templates)
    loginStage2(device, templates, email, password)

    print(f"Logged in as {email}")



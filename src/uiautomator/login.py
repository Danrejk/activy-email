from utils.clickNodeByClassInstance import clickNodeByClassInstance
from utils.setNodeTextByClassInstance import setNodeTextByClassInstance

def loginStage1(device):
    """
    Stage 1: Click the login button.
    """
    clickNodeByClassInstance(device, "android.view.View", 8)

    device(className="android.widget.EditText").wait(timeout=10)
    print("Stage 1 completed")

def loginStage2(device, email, password):
    """
    Stage 2: Put in credentials and log in.
    """
    setNodeTextByClassInstance(device, "android.widget.EditText", 0, email)
    setNodeTextByClassInstance(device, "android.widget.EditText", 1, password)
    clickNodeByClassInstance(device, "android.view.View", 7, 2)

    print("Stage 2 completed")

def Login(device, email, password):
    loginStage1(device)
    loginStage2(device, email, password)

    print(f"Logged in as f{email}")



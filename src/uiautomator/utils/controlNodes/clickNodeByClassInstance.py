from src.uiautomator.utils.controlNodes.waitForElement import waitForElement

def clickNodeByClassInstance(device, className, instance):
    node = waitForElement(device, className=className, instance=instance)
    node.click()

    return node
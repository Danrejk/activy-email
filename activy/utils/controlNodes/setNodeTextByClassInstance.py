from activy.utils.controlNodes.clickNodeByClassInstance import clickNodeByClassInstance

def setNodeTextByClassInstance(device, className, instance, text):
    node = clickNodeByClassInstance(device, className, instance)
    node.set_text(text, timeout=50)
    device.press("back")

    return node

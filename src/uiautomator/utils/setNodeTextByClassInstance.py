from .clickNodeByClassInstance import clickNodeByClassInstance

def setNodeTextByClassInstance(device, className, instance, text):
    node = clickNodeByClassInstance(device, className, instance)
    node.set_text(text)
    device.press("back")

    return node

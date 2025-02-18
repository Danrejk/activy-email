from .clickNodeByClassInstance import clickNodeByClassInstance

def setNodeTextByClassInstance(device, className, instance, text, child=None):
    node = clickNodeByClassInstance(device, className, instance, child)
    node.set_text(text)
    device.press("back")

    return node

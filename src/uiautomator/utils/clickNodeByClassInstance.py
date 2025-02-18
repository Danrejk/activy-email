def clickNodeByClassInstance(device, className, instance):
    node = device(className=className, instance=instance)
    node.wait(timeout=10)
    node.click()

    return node

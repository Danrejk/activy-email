def clickNodeByClassInstance(device, className, instance):
    node = device(className=className, instance=instance)
    node.click()

    return node

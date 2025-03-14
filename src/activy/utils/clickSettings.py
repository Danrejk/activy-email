def clickSettings(device):
    # this has to be done with proportions to click in a specific area where the tab selector is
    # the challange button is an imageView which has a varries ammount of instances
    width = device.info["displayWidth"]
    height = device.info["displayHeight"]
    x = int(width * 12 / 13)
    y = int(100)
    device.click(x, y)

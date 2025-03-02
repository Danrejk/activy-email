def getCurrentlyOpenApp(device):
    device_info = device.info
    current_package = device_info.get("currentPackageName")

    if not current_package:
        raise ValueError("Could not retrieve the currently open app.")

    return current_package

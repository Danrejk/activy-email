import time

def waitForElement(device, className, instance, timeout=20, interval=0.5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        element = device(className=className, instance=instance)
        if element.exists:
            return element
        time.sleep(interval)
    raise Exception(f"Element {className} instance {instance} not found within {timeout} seconds")

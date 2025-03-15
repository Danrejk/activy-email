import time

def waitForElement(device, className=None, instance=None, text=None, timeout=20, interval=0.5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if text is not None:
            element = device(text=text)
        else:
            element = device(className=className, instance=instance)
        if element.exists:
            return element
        time.sleep(interval)
    search_criteria = f"text={text}" if text else f"className={className}, instance={instance}"
    raise Exception(f"Element with {search_criteria} not found within {timeout} seconds")
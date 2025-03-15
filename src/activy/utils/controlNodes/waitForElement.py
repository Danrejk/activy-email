import time


def waitForElement(device, className=None, instance=None, text=None, contentDesc=None, timeout=20, interval=0.5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if text is not None:
                element = device(text=text)
            elif contentDesc is not None:
                # Search for elements with content description that contains the specified text
                element = device(descriptionContains=contentDesc)
            else:
                element = device(className=className, instance=instance)

            if element.exists:
                return element
        except Exception:
            pass
        time.sleep(interval)

    # Construct search criteria for error message
    if text is not None:
        search_criteria = f"text={text}"
    elif contentDesc is not None:
        search_criteria = f"contentDesc contains {contentDesc}"
    else:
        search_criteria = f"className={className}, instance={instance}"

    raise Exception(f"Element with {search_criteria} not found within {timeout} seconds")
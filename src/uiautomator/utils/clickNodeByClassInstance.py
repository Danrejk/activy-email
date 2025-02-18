from .waitForElement import waitForElement

def clickNodeByClassInstance(device, className, instance, child=None):
    # Wait for the element to be available
    node = waitForElement(device, className, instance, timeout=20)
    # If a child index is provided, retrieve that child using indexing
    if child is not None:
        try:
            node = node[child]
        except Exception as e:
            print(f"Error accessing child {child} of instance {instance}: {e}")
            raise
    node.click()
    return node

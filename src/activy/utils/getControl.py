import cv2
import tempfile
import os

def getControl(device, templates, expectedControl, threshold=0.7, debug=False):
    """
    Detects a specific control element on the screen.
    Accepts expectedControl as a string, list, or int.
    Returns the center coordinates of the expected control if found, else None.
    """
    # Zorg ervoor dat expectedControl een lijst is
    if isinstance(expectedControl, (list, tuple)):
        expectedControlList = [str(item) for item in expectedControl]
    else:
        expectedControlList = [str(expectedControl)]

    if debug:
        screenshotPath = "screen.png"
    else:
        screenshotPath = tempfile.mktemp(suffix=".png")

    device.screenshot(screenshotPath)

    screen = cv2.imread(screenshotPath, cv2.IMREAD_COLOR)
    screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    bestMatch = None
    bestScore = 0
    bestCoordinates = None

    for controlName in expectedControlList:
        if controlName not in templates:
            continue  # Skip als de template niet bestaat

        template = templates[controlName]
        result = cv2.matchTemplate(screenGray, template, cv2.TM_CCOEFF_NORMED)
        _, maxVal, _, maxLoc = cv2.minMaxLoc(result)

        if debug:
            print(f"Control {controlName}: Match confidence = {maxVal:.2f}")

        if maxVal > bestScore and maxVal >= threshold:
            bestMatch = controlName
            bestScore = maxVal
            templateHeight, templateWidth = template.shape[:2]
            bestCoordinates = (maxLoc[0] + templateWidth // 2, maxLoc[1] + templateHeight // 2)

    if debug:
        if bestMatch is None:
            print(f"No control found above threshold ({threshold})")
        else:
            print(f"Best match: {bestMatch}, Certainty: {bestScore:.2f}, Center: {bestCoordinates}")

    if not debug:
        os.remove(screenshotPath)

    return bestCoordinates

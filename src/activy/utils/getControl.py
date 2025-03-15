import cv2
import tempfile
import os

def getControl(device, templates, threshold=0.7, debug=False):
    """
    Detects a control element on the screen based on provided templates.
    Returns the center coordinates of the best-matching template or None if no match is found.
    """
    if debug:
        screenshot_path = "screen.png"
    else:
        screenshot_path = tempfile.mktemp(suffix=".png")

    device.screenshot(screenshot_path)

    screen = cv2.imread(screenshot_path, cv2.IMREAD_COLOR)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    best_match = None
    best_score = 0
    best_center = None

    for control_name, template in templates.items():
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if debug:
            print(f"Control {control_name}: Match confidence = {max_val:.2f}")

        if max_val > best_score and max_val >= threshold:
            best_match = control_name
            best_score = max_val
            template_height, template_width = template.shape[:2]
            best_center = (max_loc[0] + template_width // 2, max_loc[1] + template_height // 2)

    if debug:
        if best_match is None:
            print(f"No control found above threshold ({threshold})")
        else:
            print(f"Best match: {best_match}, Certainty: {best_score:.2f}, Center: {best_center}")

    if not debug:
        os.remove(screenshot_path)

    return best_center if best_center else None

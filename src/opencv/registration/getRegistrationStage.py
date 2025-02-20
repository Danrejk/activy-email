from pathlib import Path
import cv2


def load_templates(template_dir):
    templates = {}
    template_path = Path(template_dir)
    for file in template_path.glob("*.png"):
        try:
            stage_number = int(file.stem)
            img = cv2.imread(str(file), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                templates[stage_number] = img
            else:
                print(f"Failed to load image: {file}")
        except Exception as e:
            print(f"Error loading {file}: {e}")
    return templates


def getRegistrationStage(device, templates, debug=False):
    """
    Takes a screenshot and matches it against the preloaded templates.
    Returns the detected stage number or None if no match is found.
    """
    screenshot_path = "screen.png"

    if debug:
        device.screenshot(screenshot_path)

    screen = cv2.imread(screenshot_path, cv2.IMREAD_COLOR)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    best_match = None
    best_score = 0

    for stage_number, template in templates.items():
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        if max_val > best_score:
            best_score = max_val
            best_match = stage_number

    return best_match

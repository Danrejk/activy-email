import cv2
from pathlib import Path
import tempfile
import os

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

def getStage(device, templates, threshold=0.5, debug=False):
    """
    Takes a screenshot and matches it against the preloaded templates.
    Returns a tuple (detected stage number, confidence score) or None if no match is found.
    """
    if debug:
        screenshot_path = "screen.png"  # Permanent file when debugging
    else:
        screenshot_path = tempfile.mktemp(suffix=".png")  # Temporary file

    device.screenshot(screenshot_path)

    screen = cv2.imread(screenshot_path, cv2.IMREAD_COLOR)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    best_match = None
    best_score = 0
    highest_certainty = 0  # Track highest certainty

    for stage_number, template in templates.items():
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        if max_val > best_score:
            best_score = max_val
            best_match = stage_number

        if max_val > highest_certainty:
            highest_certainty = max_val

        if debug:
            print(f"Stage {stage_number}: Match confidence = {max_val:.2f}")

    if debug:
        if best_score < threshold:
            print(f"Confidence below threshold: {threshold}. No match found.")
        else:
            print(f"Best match: Stage {best_match}, Certainty: {best_score:.2f}")
        print(f"Highest certainty encountered: {highest_certainty:.2f}")

    if best_score < threshold:
        if debug:
            print(f"Returning None because confidence ({best_score:.2f}) is below threshold ({threshold}).")
        return None

    if not debug:
        os.remove(screenshot_path)

    return best_match, best_score

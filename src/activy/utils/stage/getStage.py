import cv2
import tempfile
import os


def getStage(device, templates, threshold=0.7, debug=False, ignored_stage=None):
    """
    Extension of getStage that supports ignoring specific stages.
    Returns the highest-scoring non-ignored stage, or None if no match is found.
    """
    # Convert ignored_stage to list if it's a single value
    if ignored_stage is not None and not isinstance(ignored_stage, (list, tuple)):
        ignored_stage = [str(ignored_stage)]
    elif ignored_stage is not None:
        ignored_stage = [str(item) for item in ignored_stage]
    else:
        ignored_stage = []

    import cv2
    import tempfile
    import os
    from pathlib import Path

    if debug:
        screenshot_path = "screen.png"  # Permanent file when debugging
    else:
        screenshot_path = tempfile.mktemp(suffix=".png")  # Temporary file

    device.screenshot(screenshot_path)

    screen = cv2.imread(screenshot_path, cv2.IMREAD_COLOR)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Store all match results to find non-ignored stages
    all_matches = []

    for stage_number, template in templates.items():
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        all_matches.append((stage_number, max_val))

        if debug:
            print(f"Stage {stage_number}: Match confidence = {max_val:.2f}")

    # Sort matches by score in descending order
    all_matches.sort(key=lambda x: x[1], reverse=True)

    # Find the highest non-ignored match
    best_match = None
    best_score = 0

    for stage_number, score in all_matches:
        if score < threshold:
            break  # No need to check further as scores are in descending order

        if stage_number not in ignored_stage:
            best_match = stage_number
            best_score = score
            break

    if debug:
        if best_match is None:
            if all_matches and all_matches[0][1] >= threshold:
                top_match, top_score = all_matches[0]
                print(f"Top match {top_match} (score: {top_score:.2f}) was ignored")
            else:
                print(f"No match above threshold ({threshold}) found")
        else:
            print(f"Best non-ignored match: Stage {best_match}, Certainty: {best_score:.2f}")

    if best_match is None:
        if debug:
            print("Returning None because no valid match was found.")
        return None

    if not debug:
        os.remove(screenshot_path)

    return best_match, best_score
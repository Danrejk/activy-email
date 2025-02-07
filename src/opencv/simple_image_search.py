import cv2
import numpy as np
import pyautogui
import time

def find_image_on_screen(template_path, threshold=0.8):
    """
    Search for an image on the screen and log its position if found.

    :param template_path: Path to the image file to search for.
    :param threshold: Confidence threshold for matching (default is 0.8).
    """
    # Load the template image
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"Error: Unable to load image from {template_path}")
        return

    # Get the screen resolution
    screen_width, screen_height = pyautogui.size()

    # Take a screenshot of the screen
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Check if the match is above the threshold
    if max_val >= threshold:
        print(f"Image found at position: {max_loc} with confidence: {max_val:.2f}")
    else:
        print("Image not found on the screen.")

if __name__ == "__main__":
    # Path to the image you want to search for
    template_image_path = "github_dashboard.png"  # Replace with your image path

    # Call the function to search for the image
    find_image_on_screen(template_image_path)
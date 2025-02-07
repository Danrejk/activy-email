import cv2
import numpy as np
import pyautogui

def find_image_on_screen(template_path, threshold=0.8):
    """
    Search for an image on the screen, log its position if found, and display a window highlighting the match.

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

        # Get the dimensions of the template image
        template_height, template_width = template.shape[:2]

        # Draw a rectangle around the detected area
        top_left = max_loc
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)  # Green rectangle with thickness 2

        # Calculate the center of the rectangle (middle of the detected object)
        center_x = top_left[0] + template_width // 2
        center_y = top_left[1] + template_height // 2

        # Draw a red dot at the center of the detected object
        cv2.circle(screenshot, (center_x, center_y), 5, (0, 0, 255), -1)  # Red dot with radius 5

        # Display the screenshot with the detected area and red dot
        cv2.imshow("Detected Image", screenshot)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()
    else:
        print("Image not found on the screen.")

if __name__ == "__main__":
    # Path to the image you want to search for
    template_image_path = "github_dashboard.png"  # Replace with your image path

    # Call the function to search for the image
    find_image_on_screen(template_image_path)

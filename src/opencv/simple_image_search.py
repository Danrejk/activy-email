import cv2
import numpy as np
import pyautogui


def find_image_on_screen(template_path, threshold=0.8):
    """
    Continuously search for an image on the screen, log its position if found, and display the result in a live feed.

    :param template_path: Path to the image file to search for.
    :param threshold: Confidence threshold for matching (default is 0.8).
    """
    # Load the template image
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"Error: Unable to load image from {template_path}")
        return

    # Get the template dimensions
    template_height, template_width = template.shape[:2]

    # Create a window to display the live feed
    cv2.namedWindow("Live Image Detection", cv2.WINDOW_NORMAL)

    while True:
        # Take a screenshot of the screen
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Check if the match is above the threshold
        if max_val >= threshold:
            print(f"Image found at position: {max_loc} with confidence: {max_val:.2f}")

            # Get the coordinates of the matched area
            top_left = max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

            # Draw a rectangle around the detected area
            cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)  # Green rectangle with thickness 2

            # Calculate the center of the rectangle (middle of the detected object)
            center_x = top_left[0] + template_width // 2
            center_y = top_left[1] + template_height // 2

            # Draw a red dot at the center of the detected object
            cv2.circle(screenshot, (center_x, center_y), 5, (0, 0, 255), -1)  # Red dot with radius 5
        else:
            print("Image not found on the screen.")

        # Display the screenshot with the detected area and red dot in the same window
        cv2.imshow("Live Image Detection", screenshot)

        # Exit the loop if the user presses the 'Esc' key
        if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII value for the ESC key
            break

    # Close the OpenCV window
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Path to the image you want to search for
    template_image_path = "github_dashboard.png"  # Replace with your image path

    # Call the function to search for the image in a live feed
    find_image_on_screen(template_image_path)

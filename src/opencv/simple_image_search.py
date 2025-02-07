import cv2
import numpy as np
import pyautogui

def find_image_on_screen(template_path, threshold=0.8):
    """
    Search for an image on the screen in real-time, display its position and confidence below the rectangle and circle.

    :param template_path: Path to the image file to search for.
    :param threshold: Confidence threshold for matching (default is 0.8).
    """
    # Load the template image
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"Error: Unable to load image from {template_path}")
        return

    # Get the dimensions of the template image
    template_height, template_width = template.shape[:2]

    # Create a named window for displaying the live feed
    cv2.namedWindow("Live Feed", cv2.WINDOW_NORMAL)

    font = cv2.FONT_HERSHEY_PLAIN  # Use plain for a clean computer-like font
    font_scale = 0.8
    thickness = 1  # Make the font thicker

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

            # Draw a rectangle around the detected area (green color)
            top_left = max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
            cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)  # Green rectangle with thickness 2

            # Calculate the center of the rectangle (middle of the detected object)
            center_x = top_left[0] + template_width // 2
            center_y = top_left[1] + template_height // 2

            # Draw a red dot at the center of the detected object
            cv2.circle(screenshot, (center_x, center_y), 5, (0, 0, 255), -1)  # Red dot with radius 5

            # Display the coordinates of the rectangle (green text)
            coords_text = f"POS: {max_loc}"
            coords_text_size = cv2.getTextSize(coords_text, font, font_scale, thickness)[0]
            coords_text_x = top_left[0]
            coords_text_y = bottom_right[1] + 20  # Position the text 20px below the rectangle
            cv2.putText(screenshot, coords_text, (coords_text_x, coords_text_y), font, font_scale, (0, 255, 0), thickness)

            # Display the confidence below the coordinates (green text)
            confidence_text = f"CONF: {max_val:.2f}"
            confidence_text_size = cv2.getTextSize(confidence_text, font, font_scale, thickness)[0]
            confidence_text_x = top_left[0]
            confidence_text_y = coords_text_y + 20  # Position the text 20px below the coordinates
            cv2.putText(screenshot, confidence_text, (confidence_text_x, confidence_text_y), font, font_scale, (0, 255, 0), thickness)

            # Display the coordinates below the circle (red text)
            circle_text = f"({center_x}, {center_y})"
            circle_text_size = cv2.getTextSize(circle_text, font, font_scale, thickness)[0]
            circle_text_x = center_x - circle_text_size[0] // 2  # Center the text below the circle
            circle_text_y = center_y + 20  # Position the text 20px below the circle
            cv2.putText(screenshot, circle_text, (circle_text_x, circle_text_y), font, font_scale, (0, 0, 255), thickness)

        # Display the screenshot with the detected area and red dot
        cv2.imshow("Live Feed", screenshot)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the window and destroy all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Path to the image you want to search for
    template_image_path = "github_dashboard.png"  # Replace with your image path

    # Call the function to search for the image in real-time
    find_image_on_screen(template_image_path)

import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
from threading import Thread
import time
from collections import deque


def find_image_on_screen(template_path, threshold=0.8, scale_range=(0.5, 2.0), scale_steps=10):
    """
    Search for an image within the Opera browser window in real-time with scale invariance.

    :param template_path: Path to the image file to search for.
    :param threshold: Confidence threshold for matching (default is 0.8).
    :param scale_range: Tuple (min_scale, max_scale) for scaling search range.
    :param scale_steps: Number of scale steps between min and max scale.
    """
    # Load and precompute scaled templates
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"Error: Unable to load image from {template_path}")
        return

    template_height, template_width = template.shape[:2]
    scales = np.linspace(scale_range[0], scale_range[1], scale_steps)

    # Pre-compute scaled templates
    scaled_templates = {}
    for scale in scales:
        scaled_w = int(template_width * scale)
        scaled_h = int(template_height * scale)
        scaled_templates[scale] = cv2.resize(template, (scaled_w, scaled_h),
                                             interpolation=cv2.INTER_AREA)

    # Initialize screenshot buffer and FPS tracking
    screenshot_buffer = deque(maxlen=1)
    running = True
    fps_buffer = deque(maxlen=30)
    last_time = time.time()

    # Font settings (matching original)
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 1.5
    thickness = 2

    def capture_screenshots():
        """Continuously capture screenshots in a separate thread"""
        while running:
            opera_windows = [w for w in gw.getWindowsWithTitle("Opera")]
            if opera_windows and opera_windows[0].isActive:
                window = opera_windows[0]
                screenshot = pyautogui.screenshot(region=(window.left, window.top,
                                                          window.width, window.height))
                screenshot_buffer.append((cv2.cvtColor(np.array(screenshot),
                                                       cv2.COLOR_RGB2BGR),
                                          window.width, window.height))
            time.sleep(0.01)  # Small delay to prevent excessive CPU usage

    # Create window and start capture thread
    cv2.namedWindow("Live Feed", cv2.WINDOW_NORMAL)
    capture_thread = Thread(target=capture_screenshots)
    capture_thread.start()

    try:
        while running:
            current_time = time.time()

            # Handle no Opera window case
            if not screenshot_buffer:
                black_screen = np.zeros((500, 800, 3), dtype=np.uint8)
                warning_text = "Opera window is not open or not in focus!"
                text_size = cv2.getTextSize(warning_text, font, font_scale, thickness)[0]
                text_x = (800 - text_size[0]) // 2
                text_y = (500 + text_size[1]) // 2
                cv2.putText(black_screen, warning_text, (text_x, text_y), font,
                            font_scale, (0, 0, 255), thickness)
                cv2.imshow("Live Feed", black_screen)
            else:
                screenshot, width, height = screenshot_buffer[0]

                # Template matching with precomputed scales
                best_max_val = -1
                best_max_loc = None
                best_scale = 1.0
                best_scaled_size = (template_width, template_height)

                # Convert to grayscale once for efficiency
                gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

                for scale, scaled_template in scaled_templates.items():
                    scaled_w, scaled_h = scaled_template.shape[1], scaled_template.shape[0]

                    if scaled_w > width or scaled_h > height:
                        continue

                    gray_template = cv2.cvtColor(scaled_template, cv2.COLOR_BGR2GRAY)
                    result = cv2.matchTemplate(gray_screenshot, gray_template,
                                               cv2.TM_CCORR_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                    if max_val > best_max_val:
                        best_max_val = max_val
                        best_max_loc = max_loc
                        best_scale = scale
                        best_scaled_size = (scaled_w, scaled_h)

                # Draw detection results (matching original style)
                if best_max_val >= threshold:
                    top_left = best_max_loc
                    bottom_right = (top_left[0] + best_scaled_size[0],
                                    top_left[1] + best_scaled_size[1])

                    # Green rectangle around match
                    cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)

                    # Red center point
                    center_x = top_left[0] + best_scaled_size[0] // 2
                    center_y = top_left[1] + best_scaled_size[1] // 2
                    cv2.circle(screenshot, (center_x, center_y), 5, (0, 0, 255), -1)

                    # Text information (matching original style and position)
                    texts = [
                        f"POS: {top_left}",
                        f"CONF: {best_max_val:.2f}",
                        f"SCALE: {best_scale:.2f}",
                        f"CENTER: ({center_x}, {center_y})"
                    ]

                    y_offset = bottom_right[1] + 20
                    for text in texts:
                        cv2.putText(screenshot, text, (top_left[0], y_offset),
                                    font, font_scale, (0, 255, 0), thickness)
                        y_offset += 20

                # Calculate and display FPS
                fps_buffer.append(1 / (current_time - last_time))
                avg_fps = sum(fps_buffer) / len(fps_buffer)
                cv2.putText(screenshot, f"FPS: {avg_fps:.1f}", (10, 30),
                            font, font_scale, (0, 255, 0), thickness)

                cv2.imshow("Live Feed", screenshot)
                last_time = current_time

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        running = False
        capture_thread.join()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    find_image_on_screen("github_dashboard.png", scale_range=(0.5, 2.0), scale_steps=10)
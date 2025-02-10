import cv2
import numpy as np
import platform
import mss
import threading
import time


class ScreenMonitor:
    def __init__(self, template_path=None, threshold=0.8):
        """
        Initialize screen monitoring with optional template matching

        :param template_path: Path to template image for matching
        :param threshold: Confidence threshold for template matching
        """
        self.template_path = template_path
        self.threshold = threshold
        self.is_running = False

        self.template = None
        if template_path:
            self.template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if self.template is None:
                print(f"Error: Unable to load template from {template_path}")

    def capture_screen(self):
        """Capture screen using mss"""
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))
            return cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    def monitor(self):
        """
        Real-time screen monitoring with optional template matching
        """
        self.is_running = True

        if self.template is not None:
            template_height, template_width = self.template.shape[:2]

        cv2.namedWindow("Screen Monitor", cv2.WINDOW_NORMAL)

        while self.is_running:
            # Capture screen
            screenshot = self.capture_screen()

            # Template matching if template provided
            if self.template is not None:
                result = cv2.matchTemplate(screenshot, self.template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)

                if max_val >= self.threshold:
                    top_left = max_loc
                    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

                    cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
                    cv2.putText(screenshot, f"Confidence: {max_val:.2f}",
                                (top_left[0], top_left[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow("Screen Monitor", screenshot)

            # Exit on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


def main():
    # Optional: Specify template image path
    template_path = "github_dashboard.png"  # Replace with your template

    monitor = ScreenMonitor(template_path)
    monitor.monitor()


if __name__ == "__main__":
    main()
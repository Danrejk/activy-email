import cv2
import numpy as np
import pytesseract
import mss


class TextDetector:
    def detect_text(self, screenshot):
        # Convert to grayscale and enhance contrast
        gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Specific configurations for login page text
        custom_config = r'--oem 3 --psm 6'

        try:
            # Detailed text detection with custom config
            details = pytesseract.image_to_data(gray, config=custom_config, output_type=pytesseract.Output.DICT)

            # Print all detected text with confidence
            for i in range(len(details['text'])):
                if details['text'][i].strip() and int(details['conf'][i]) > 0:
                    print(f"Detected: '{details['text'][i]}' (Conf: {details['conf'][i]}))")

        except Exception as e:
            print(f"OCR Error: {e}")

    def monitor(self):
        with mss.mss() as sct:
            while True:
                # Capture screen
                screenshot = np.array(sct.grab(sct.monitors[0]))
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGBA2RGB)

                # Detect text
                self.detect_text(screenshot)

                cv2.imshow('Debug', screenshot)
                if cv2.waitKey(1000) & 0xFF == ord('q'):
                    break


if __name__ == "__main__":
    detector = TextDetector()
    detector.monitor()
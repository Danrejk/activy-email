from pathlib import Path
import cv2

def load_templates(template_dir):
    templates = {}
    template_path = Path(template_dir)
    for file in template_path.glob("*.png"):
        try:
            stage_key = file.stem
            img = cv2.imread(str(file), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                templates[stage_key] = img
            else:
                print(f"Failed to load image: {file}")
        except Exception as e:
            print(f"Error loading {file}: {e}")
    return templates
import cv2
import numpy as np
import uiautomator2 as u2
from xml.etree import ElementTree as ET

# Connect to the device (ensure device is connected via ADB)
device = u2.connect()  # Use the appropriate IP if using a remote device


def drawNodeBoundaries():
    # Capture the current UI hierarchy from the device
    hierarchy_xml = device.dump_hierarchy()

    # Parse the XML data to get node information
    root = ET.fromstring(hierarchy_xml)

    nodes = []

    # Loop through all nodes in the hierarchy and extract their bounds
    for node in root.findall(".//node"):
        # Get the bounds and other relevant attributes
        bounds = node.attrib.get('bounds', '')
        class_name = node.attrib.get('class', '')
        instance = node.attrib.get('index', '')  # This will be used as the instance

        if bounds:
            # The bounds are in the format "[x1,y1][x2,y2]"
            # We need to extract (x1, y1, x2, y2) from this
            bounds = bounds.replace("][", ",").replace("[", "").replace("]", "").split(",")
            x1, y1, x2, y2 = map(int, bounds)

            # Add the node to the list with extra attributes
            nodes.append({
                'x': x1,
                'y': y1,
                'width': x2 - x1,
                'height': y2 - y1,
                'class': class_name,
                'instance': instance  # Use the index as the instance
            })

    # Capture a screenshot of the device (not the full screen)
    screenshot = device.screenshot()

    # Convert the screenshot (PIL image) to a numpy array for OpenCV to process
    img = np.array(screenshot)

    # Convert RGB to BGR (OpenCV uses BGR by default)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Loop over the nodes and draw boundaries (rectangles)
    for node in nodes:
        # Extract node properties
        x, y, w, h = node['x'], node['y'], node['width'], node['height']

        # Draw a rectangle around the node
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color, 2 thickness

        # Display class and instance below the class name
        label = f"{node['instance']}:{node['class']}"

        # Define font and size for the label
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.2  # Even smaller font size
        font_thickness = 1
        outline_thickness = 1  # Thickness of outline

        # Calculate text size
        (text_width, text_height), _ = cv2.getTextSize(label, font, font_scale, font_thickness)

        # Draw text outline (black color) to create an outline effect
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                cv2.putText(img, label, (x + 5 + dx, y + 25 + dy), font, font_scale, (0, 0, 0), outline_thickness,
                            cv2.LINE_AA)

        # Draw the main text (white color)
        cv2.putText(img, label, (x + 5, y + 25), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    # Save the image with the drawn boundaries to a file
    cv2.imwrite("nodes.png", img)

    # Optionally, display the image
    cv2.imshow("Device Screenshot with Node Boundaries", img)

    # Wait until a key is pressed and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Call the function to capture and draw boundaries from the device's UI hierarchy
drawNodeBoundaries()

import cv2
import numpy as np
import uiautomator2 as u2
from xml.etree import ElementTree as ET


def drawNodeBoundaries(device):
    # Capture the current UI hierarchy from the device
    hierarchy_xml = device.dump_hierarchy()

    # Parse the XML data to get node information
    root = ET.fromstring(hierarchy_xml)

    nodes = []
    class_instances = {}  # Dictionary to track counts per class

    def traverse(node):
        # Retrieve the class and bounds of the current node
        node_class = node.attrib.get('class', '')
        bounds = node.attrib.get('bounds', '')

        if bounds and node_class:
            # Parse the bounds string "[x1,y1][x2,y2]"
            parts = bounds.replace("][", ",").replace("[", "").replace("]", "").split(",")
            x1, y1, x2, y2 = map(int, parts)

            # Assign a unique instance number for this class
            if node_class not in class_instances:
                class_instances[node_class] = 0
            instance = class_instances[node_class]
            class_instances[node_class] += 1

            nodes.append({
                'x': x1,
                'y': y1,
                'width': x2 - x1,
                'height': y2 - y1,
                'class': node_class,
                'instance': instance  # Instance number for this class
            })

        # Recursively traverse child nodes
        for child in node.findall('node'):
            traverse(child)

    # Start traversing from the root of the hierarchy
    traverse(root)

    # Capture a screenshot of the device (not the full screen)
    screenshot = device.screenshot()

    # Convert the screenshot (PIL image) to a numpy array for OpenCV processing
    img = np.array(screenshot)
    # Convert RGB to BGR (OpenCV uses BGR by default)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Loop over the nodes and draw boundaries (rectangles)
    for node in nodes:
        x, y, w, h = node['x'], node['y'], node['width'], node['height']

        # Draw a rectangle around the node
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color, 2 thickness

        # Prepare the label as "instance:class"
        label = f"{node['instance']}:{node['class']}"

        # Define font and size for the label
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.2
        font_thickness = 1
        outline_thickness = 1

        # Draw text outline (black) for better readability
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                cv2.putText(img, label, (x + 5 + dx, y + 25 + dy), font, font_scale, (0, 0, 0), outline_thickness,
                            cv2.LINE_AA)
        # Draw the main text (white)
        cv2.putText(img, label, (x + 5, y + 25), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    # Save the image with drawn boundaries to a file
    cv2.imwrite("nodes.png", img)

    # Optionally, display the image
    cv2.imshow("Device Screenshot with Node Boundaries", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

from io import BytesIO
from PIL import Image

def imageToBlob(image_path):
    with open(image_path, "rb") as file:
        return file.read()

def blobToImage(blob_data):
    return Image.open(BytesIO(blob_data))

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
def preprocess_image(image_path):

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Noise removal
    denoised = cv2.medianBlur(binary, 3)

    # Dilate to connect broken handwriting strokes
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(denoised, kernel, iterations=1)

    # Resize if too small
    height, width = dilated.shape
    if width < 1000:
        scale = 1000 / width
        new_width = int(width * scale)
        new_height = int(height * scale)
        dilated = cv2.resize(dilated, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    return dilated


def preprocess_with_pil(image_path):

    image = Image.open(image_path)

    # Convert to grayscale
    if image.mode != 'L':
        image = image.convert('L')

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # Sharpen
    image = image.filter(ImageFilter.SHARPEN)

    # Resize
    if image.width < 800:
        ratio = 800 / image.width
        new_size = (800, int(image.height * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)

    return image
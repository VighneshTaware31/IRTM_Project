import easyocr
import numpy as np
from PIL import Image

reader = easyocr.Reader(['en'])

def extract_text_from_image(image):
    try:
        img_array = np.array(image)
        result = reader.readtext(img_array, detail=0)
        return " ".join(result)
    except Exception as e:
        return f"OCR Error: {e}"
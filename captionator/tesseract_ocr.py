import cv2
from pathlib import Path
import pytesseract
import numpy as np


class OCR:
    def __init__(self, _config, files):
        self._paths = files

    def as_text(self):
        return '/n'.join(
            self._convert_one(path) for path in map(Path, self._paths)
            if path.exists() and (path.match('*.png') or path.match('*.jpg'))
        )

    @staticmethod
    def _get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def _remove_noise(image):
        return cv2.medianBlur(image, 5)

    @staticmethod
    def _thresholding(image):
        return cv2.threshold(image, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    @staticmethod
    def _dilate(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)

    @staticmethod
    def _erode(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1)

    @staticmethod
    def _opening(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    @staticmethod
    def _canny(image):
        return cv2.Canny(image, 100, 200)

    def _convert_one(self, image_path):
        image = cv2.imread(str(image_path))
        gray = self._get_grayscale(image)
        thresh, img_bin = self._thresholding(gray)
        bit_not = cv2.bitwise_not(img_bin)
        opening = self._erode(bit_not)
        canny = self._dilate(opening)

        custom_config = r'-l eng --psm 6'
        out_below = pytesseract.image_to_string(gray, config=custom_config)
        return out_below


if __name__ == "__main__":
    print(OCR(None, ["test.png"]).as_text())

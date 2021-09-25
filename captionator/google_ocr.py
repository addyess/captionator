import io
import os
from google.cloud import vision
from pathlib import Path


class OCR:
    def __init__(self, config, files):
        self._paths = files
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(
            next(Path(config.google_keydir).glob("*.json"))
        )

    def as_text(self):
        return "/n".join(
            self._convert_one(path)
            for path in map(Path, self._paths)
            if path.exists() and (path.match("*.png") or path.match("*.jpg"))
        )

    def _convert_one(self, image_path):
        client = vision.ImageAnnotatorClient()
        file_name = os.path.abspath(image_path)
        with io.open(file_name, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        return texts[0].description


if __name__ == "__main__":

    class Config:
        google_keydir = "keys"

    print(OCR(Config, ["test.png"]).as_text())

import argparse
from pathlib import Path
from captionator.config import Config
from captionator.server import WebUX
from captionator.google_ocr import OCR


def parseargs():
    parser = argparse.ArgumentParser("captionator")
    parser.add_argument("--mysql_host", default="localhost")
    parser.add_argument("--mysql_user", default="username")
    parser.add_argument("--mysql_pass", default="password")
    parser.add_argument("--http_port", default=8080)
    parser.add_argument("--google_keydir", default="keys")
    return parser.parse_args()


if __name__ == '__main__':
    config = Config.get() or parseargs()
    WebUX(config, OCR).main()

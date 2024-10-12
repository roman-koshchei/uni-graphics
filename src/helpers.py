from PIL import Image
import os


def filename(path: str):
    return os.path.splitext(os.path.basename(path))[0]


def save_img(img: Image.Image, name: str, dir: str):
    img.save(
        dir + name + ".png",
        "PNG",
    )

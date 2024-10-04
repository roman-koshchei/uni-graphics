import argparse
from typing import List, Tuple
from PIL import Image, ImageEnhance, ImageDraw
import os


# python3 ./src/lab_2.py ./images/town.jpg --opacity 0.2 --crop 1000 50 3000 1500 --contrast 1.5 --rows 2 --cols 2 --cutout 1500 100 2200 1300


def opacity(img: Image.Image, value: float) -> Image.Image:
    opacity = round(value * 255)
    if not (0 <= opacity <= 255):
        return img

    img.putalpha(opacity)
    return img


def split(img: Image.Image, cols: int, rows: int) -> List[Image.Image]:
    tile_width = img.width // cols
    tile_height = img.height // rows

    cropped_images: List[Image.Image] = []

    for i in range(rows):
        for j in range(cols):
            left = j * tile_width
            upper = i * tile_height
            right = left + tile_width
            lower = upper + tile_height

            # Adjust right and lower to not exceed image dimensions
            right = min(right, img.width)
            lower = min(lower, img.height)

            # Crop the image
            box = (left, upper, right, lower)
            cropped_image = img.crop(box)
            cropped_images.append(cropped_image)

    return cropped_images


def crop(img: Image.Image, left: int, right: int, top: int, bottom: int) -> Image.Image:
    return img.crop((left, top, right, bottom))


def cutout(
    img: Image.Image, left: int, right: int, top: int, bottom: int
) -> Image.Image:
    data = img.getdata()

    new_data = []
    for y in range(img.height):
        for x in range(img.width):
            index = y * img.width + x
            r, g, b, a = data[index]

            if left <= x < right and top <= y < bottom:
                new_data.append((r, g, b, 0))
            else:
                new_data.append((r, g, b, a))

    img.putdata(new_data)
    return img


def contrast(img: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)


def filename(path: str):
    return os.path.splitext(os.path.basename(path))[0]


def save(img: Image.Image, name: str, dir: str):
    img.save(
        dir + name + ".png",
        "PNG",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Process images with resizing, color change, and color balance."
    )

    parser.add_argument("imgs_paths", nargs="+", help="Paths to the input images.")
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./images/",
        help="Directory to save processed images.",
    )

    parser.add_argument("--opacity", type=float, help="Set opacity (0.0 to 1.0).")
    parser.add_argument(
        "--crop",
        nargs=4,
        type=int,
        help="Crop the image. Provide left, upper, right, lower coordinates.",
    )
    parser.add_argument(
        "--contrast",
        type=float,
        help="Adjust contrast. Provide a factor (e.g., 1.5 for increase).",
    )

    parser.add_argument(
        "--rows", type=int, help="Number of horizontal parts to split into."
    )
    parser.add_argument(
        "--cols", type=int, help="Number of vertical parts to split into."
    )

    parser.add_argument(
        "--cutout",
        nargs=4,
        type=int,
        help="Remove pixels inside a specified area. Provide left, upper, right, lower coordinates.",
    )

    args = parser.parse_args()
    for img_path in args.imgs_paths:
        img = Image.open(img_path).convert("RGBA")

        if args.opacity is not None:
            img = opacity(img, args.opacity)

        # Apply contrast adjustment if specified
        if args.contrast is not None:
            img = contrast(img, args.contrast)

        if args.cutout is not None:
            left, upper, right, lower = args.cutout
            img = cutout(img, left, right, upper, lower)

        if args.crop is not None:
            left, upper, right, lower = args.crop
            img = crop(img, left, right, upper, lower)

        if args.rows is not None or args.cols is not None:
            rows = args.rows if args.rows is not None else 1
            cols = args.cols if args.cols is not None else 1
            cropped_images = split(img, rows, cols)

            for i, cropped_img in enumerate(cropped_images):
                save(cropped_img, f"{filename(img_path)}_{i}", args.output_dir)
        else:
            save(img, filename(img_path), args.output_dir)


if __name__ == "__main__":
    main()
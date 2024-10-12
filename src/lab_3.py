import argparse
from datetime import datetime
from typing import List, Tuple
from PIL import Image, ImageFont, ImageDraw, ImageTk
from helpers import save_img, filename
import tkinter as tk
import threading

# python3 ./src/lab_3.py ./images/town.jpg ./images/song.jpg

# python3 ./src/lab_3.py ./images/town.jpg --watermark_text "By Roman Koshchei" --watermark_position 50 50 --watermark_font_size 264 --watermark_color 255 255 255 --watermark_opacity 200

# python3 ./src/lab_3.py ./images/town.jpg ./images/song.jpg --join 1 0 --join_direction horizontal

# python3 ./src/lab_3.py ./images/town.jpg ./images/song.jpg --join 1 0 --join_direction horizontal --watermark_text "By Roman Koshchei" --watermark_position 50 50 --watermark_font_size 264 --watermark_color 255 255 255 --watermark_opacity 200


def join(image_1: Image.Image, image_2: Image.Image, is_vertical: bool) -> Image.Image:
    new_image: Image.Image

    if is_vertical:
        new_width: int
        if image_1.width > image_2.width:
            new_width = image_1.width
            image_2_height = round(image_2.height * (image_1.width / image_2.width))
            image_2 = image_2.resize((image_1.width, image_2_height))

        elif image_2.width > image_1.width:
            new_width = image_2.width
            image_1_height = round(image_1.height * (image_2.width / image_1.width))
            image_1 = image_1.resize((image_2.width, image_1_height))

        else:
            new_width = image_1.width

        new_height = image_1.height + image_2.height
        new_image = Image.new("RGB", (new_width, new_height))
        new_image.paste(image_1, (0, 0))
        new_image.paste(image_2, (0, image_1.height))
    else:
        new_height: int
        if image_1.height > image_2.height:
            new_height = image_1.height
            image_2_width = round(image_2.width * (image_1.height / image_2.height))
            image_2 = image_2.resize((image_2_width, image_1.height))

        elif image_2.height > image_1.height:
            new_height = image_2.height
            image_1_width = round(image_1.width * (image_2.height / image_1.height))
            image_1 = image_1.resize((image_1_width, image_2.height))

        else:
            new_height = image_1.height

        new_width = image_1.width + image_2.width
        new_image = Image.new("RGB", (new_width, new_height))
        new_image.paste(image_1, (0, 0))
        new_image.paste(image_2, (image_1.width, 0))

    return new_image


def watermark(
    img: Image.Image,
    text: str,
    position: Tuple[int, int],
    opacity: int = 128,
    color: Tuple[int, int, int] = (255, 255, 255),
    size: int = 30,
):
    img = img.convert("RGBA")
    font = ImageFont.load_default(size)

    text_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_layer)

    draw.text(position, text, font=font, fill=(color[0], color[1], color[2], opacity))

    return Image.alpha_composite(img, text_layer)


def fit_into(img: Image.Image, max_width: int, max_height: int) -> Image.Image:
    width_ratio = max_width / img.width
    height_ratio = max_height / img.height

    new_width: int
    new_height: int

    if width_ratio < height_ratio:
        # width difference is bigger
        new_width = max_width
        new_height = img.height * width_ratio
    else:
        new_height = max_height
        new_width = img.width * height_ratio

    return img.resize((round(new_width), round(new_height)))


def slideshow_run(
    label: tk.Label, imgs: List[Image.Image], stop_event: threading.Event
):
    current_index = 0
    time = datetime.now()

    while not stop_event.is_set():
        new_time = datetime.now()
        if (new_time - time).seconds > 1:
            time = new_time

            img = imgs[current_index]

            photo = ImageTk.PhotoImage(fit_into(img, 1000, 600))
            label.config(image=photo)
            label.image = photo

            current_index = (current_index + 1) % len(imgs)


def slideshow_close(
    root: tk.Tk, slideshow_thread: threading.Thread, stop_event: threading.Event
):
    root.quit()
    stop_event.set()
    slideshow_thread.join()


def slideshow(imgs: List[Image.Image]):
    root = tk.Tk()
    root.title("Slide show")

    label = tk.Label(root)
    label.pack()

    stop_event = threading.Event()

    # Start the slideshow thread
    slideshow_thread = threading.Thread(
        target=slideshow_run, args=(label, imgs, stop_event), daemon=True
    )
    slideshow_thread.start()

    # Handle window close
    root.protocol(
        "WM_DELETE_WINDOW", lambda: slideshow_close(root, slideshow_thread, stop_event)
    )

    # Start the main event loop
    root.mainloop()


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

    parser.add_argument("--watermark_text", "--wm_text", help="Watermark text")
    parser.add_argument(
        "--watermark_position",
        "--wm_position",
        type=int,
        nargs=2,
        default=[50, 50],
        help="Position (x, y) for the watermark",
    )
    parser.add_argument(
        "--watermark_font_size",
        "--wm_font_size",
        type=int,
        default=30,
        help="Font size of the watermark",
    )
    parser.add_argument(
        "--watermark_color",
        "--wm_color",
        type=int,
        nargs=3,
        default=[255, 255, 255],
        help="Color of the watermark in RGB",
    )
    parser.add_argument(
        "--watermark_opacity",
        "--wm_opacity",
        type=int,
        default=128,
        help="Opacity of the watermark",
    )

    parser.add_argument(
        "--join",
        type=int,
        nargs=2,
        help="Indexes of two images to join (default: 0 1)",
    )
    parser.add_argument(
        "--join_direction",
        choices=["horizontal", "vertical"],
        default="vertical",
        help="Direction to join images",
    )
    parser.add_argument(
        "--join_name",
        default="joined_image",
        help="Name of file for the joined image",
    )

    args = parser.parse_args()

    imgs_paths = args.imgs_paths
    imgs: List[Image.Image] = []

    for img_path in imgs_paths:
        img = Image.open(img_path).convert("RGBA")
        imgs.append(img)

    if args.join is not None and len(imgs) > 1:
        index_1, index_2 = args.join
        if index_1 < 0 or index_1 > len(imgs) - 1:
            index_1 = 0
        if index_2 < 0 or index_2 > len(imgs) - 1:
            index_2 = 1

        is_vertical = True
        if args.join_direction == "horizontal":
            is_vertical = False

        img_1 = imgs[index_1]
        img_2 = imgs[index_2]
        img_path_1 = imgs_paths[index_1]
        img_path_2 = imgs_paths[index_2]

        img = join(img_1, img_2, is_vertical)

        imgs.remove(img_1)
        imgs.remove(img_2)
        imgs.append(img)
        imgs_paths.remove(img_path_1)
        imgs_paths.remove(img_path_2)

        imgs_paths.append(args.join_name)

    result_imgs: List[Image.Image] = []

    for i, img in enumerate(imgs):

        if args.watermark_text is not None:

            img = watermark(
                img,
                args.watermark_text,
                args.watermark_position,
                size=args.watermark_font_size,
                color=args.watermark_color,
                opacity=args.watermark_opacity,
            )

        result_imgs.append(img)
        save_img(img, filename(imgs_paths[i]), args.output_dir)

    slideshow(result_imgs)


if __name__ == "__main__":
    main()

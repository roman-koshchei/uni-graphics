from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np

# python3 ./src/lab_4.py


def plot_img(img: Image.Image, title: str | None = None):
    plt.figure(figsize=(6, 6))
    plt.imshow(img)
    plt.axis("off")
    if title is not None:
        plt.title(title)


def calc_brightness(r: int, g: int, b: int) -> int:
    return round(0.3 * r + 0.59 * g + 0.11 * b)

def pixel_brightness(pixel: tuple[int, int, int]):
    return calc_brightness(pixel[0], pixel[1], pixel[2])


def binarization(img: Image.Image, threshold=128) -> Image.Image:
    return img.convert("L").point(lambda x: 255 if x > threshold else 0, "1")


def grayscale(img: Image.Image) -> Image.Image:
    return img.convert("1")


def negative(img: Image.Image) -> Image.Image:
    return ImageOps.invert(img)


def display_grayscale_histogram(img: Image.Image):
    grayscale_image = img.convert("L")
    plt.figure(figsize=(10, 5))
    plt.hist(np.array(grayscale_image).flatten(), bins=256, color="orange", alpha=0.5)
    plt.title("Grayscale Image Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")


def display_brightness_histogram(img: Image.Image):
    brightness_values = []
    brightness_values = [pixel_brightness(pixel) for pixel in list(img.getdata())]

    plt.figure(figsize=(10, 5))
    plt.hist(brightness_values, bins=256, color="gray", alpha=0.7)
    plt.title("Histogram of Image Brightness")
    plt.xlabel("Brightness")
    plt.ylabel("Frequency")


def display_brightness_matrix(image: Image.Image):
    brightness_matrix = [
        [pixel_brightness(image.getpixel((x, y))) for x in range(image.width)]
        for y in range(image.height)
    ]

    for row in brightness_matrix:
        print(' '.join(f'{value:5.1f}' for value in row))

def main():
    img = Image.open("./images/song.jpg").convert("RGB")

    plot_img(img, "Original Color Image")

    display_brightness_matrix(img)

    plot_img(binarization(img))

    plot_img(grayscale(img))

    plot_img(negative(img))

    display_grayscale_histogram(img)

    display_brightness_histogram(img)

    plt.show()


if __name__ == "__main__":
    main()

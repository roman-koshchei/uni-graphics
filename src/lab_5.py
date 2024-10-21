from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np

# variant 13
# python3 ./src/lab_5.py


def sigma_filter(image: Image.Image, window_size=3, sigma=200):
    pixels = np.array(image)

    # offset of window
    offset = window_size // 2
    output_pixels = np.zeros_like(pixels)

    # going through each color
    for channel in range(3):
        for i in range(offset, pixels.shape[0] - offset):
            for j in range(offset, pixels.shape[1] - offset):
                # taking window
                window = pixels[i - offset:i + offset + 1, j - offset:j + offset + 1, channel]
                center_pixel = pixels[i, j, channel]

                # determine which pixels has difference with center <= sigma
                mask = np.abs(window - center_pixel) <= sigma
                # pixels that are valid
                filtered_values = window[mask]

                # if there is valid pixels then avaraging
                if filtered_values.size > 0:
                    output_pixels[i, j, channel] = np.mean(filtered_values)
                else:
                    output_pixels[i, j, channel] = center_pixel

    output_image = Image.fromarray(output_pixels.astype(np.uint8))
    return output_image


def plot_img(img: Image.Image, title: str | None = None):
    plt.figure(figsize=(6, 6))
    plt.imshow(img)
    plt.axis("off")
    if title is not None:
        plt.title(title)


def main():
    img = Image.open("./images/pigs.jpg").convert("RGB")

    plot_img(img)
    # plot_img(sigma_filter(img, sigma=20))
    # plot_img(sigma_filter(img, sigma=200))
    # plot_img(sigma_filter(img, sigma=400))
    plot_img(sigma_filter(img, window_size=12, sigma=80))

    plt.show()


if __name__ == "__main__":
    main()

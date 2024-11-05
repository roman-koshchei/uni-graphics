from typing import List
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.ndimage import gaussian_filter, median_filter, generic_filter

# python3 ./src/lab_6.py

ImageArray = np.ndarray


def add_additive_noise(image: ImageArray, variance: float) -> ImageArray:
    noise = np.random.normal(0, variance**0.5, image.shape)
    noisy_image = np.clip(image + noise, 0, 255).astype(np.uint8)
    return noisy_image


def add_impulse_noise(
    image: ImageArray, amount: float = 0.05, salt_vs_pepper: float = 0.5
) -> ImageArray:
    noisy_image = np.copy(image)
    num_salt = int(np.ceil(amount * image.size * salt_vs_pepper))
    num_pepper = int(np.ceil(amount * image.size * (1 - salt_vs_pepper)))

    # Add salt (white) noise
    salt_coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape]
    noisy_image[salt_coords[0], salt_coords[1], :] = 255

    # Add pepper (black) noise
    pepper_coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape]
    noisy_image[pepper_coords[0], pepper_coords[1], :] = 0

    return noisy_image


def add_brightness_dependent_noise(
    image: ImageArray, base_variance: float = 30
) -> ImageArray:
    brightness = image.mean(axis=2, keepdims=True) / 255.0
    variance_map = base_variance * brightness
    noise = np.random.normal(0, variance_map**0.5, image.shape)
    noisy_image = np.clip(image + noise, 0, 255).astype(np.uint8)
    return noisy_image


def add_coordinate_dependent_noise(
    image: ImageArray, base_variance: float = 30
) -> ImageArray:
    rows, cols, _ = image.shape
    x, y = np.meshgrid(np.linspace(0, 1, cols), np.linspace(0, 1, rows))
    variance_map = base_variance * (x + y) / 2
    noise = np.random.normal(0, variance_map[..., None] ** 0.5, image.shape)
    noisy_image = np.clip(image + noise, 0, 255).astype(np.uint8)
    return noisy_image


def apply_filters(image_array: ImageArray) -> List[ImageArray]:
    return [
        # Linear Filters
        generic_filter(image_array, np.mean, size=(3, 3, 1)),  # Mean Filter
        gaussian_filter(image_array, sigma=1),  # Gaussian Filter
        median_filter(image_array, size=3),  # Median Filter
        # Nonlinear Filters
        cv2.bilateralFilter(
            image_array, d=9, sigmaColor=75, sigmaSpace=75
        ),  # Bilateral Filter
        cv2.GaussianBlur(image_array, (5, 5), 0),  # Gaussian Mixture Model Filter
        cv2.morphologyEx(
            image_array, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)
        ),  # Morphological Opening
        cv2.morphologyEx(
            image_array, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)
        ),  # Morphological Closing
        cv2.dilate(
            image_array, np.ones((5, 5), np.uint8), iterations=1
        ),  # Morphological Dilation
        cv2.erode(
            image_array, np.ones((5, 5), np.uint8), iterations=1
        ),  # Morphological Erosion
    ]


def estimate_distortion(
    initial_image_array: ImageArray, result_image_array: ImageArray
) -> float:
    return np.sum(np.abs(result_image_array - initial_image_array)) / (128 * 128)


def main():
    img = Image.open("./images/lab-6/pigs-0.bmp").convert("RGB")
    image_array = np.array(img)

    noisy_images: List[np.array] = [
        image_array,
        add_additive_noise(image_array, 20),
        add_additive_noise(image_array, 50),
        add_impulse_noise(image_array, amount=0.05),
        add_impulse_noise(image_array, amount=0.1),
        add_brightness_dependent_noise(image_array, base_variance=30),
        add_brightness_dependent_noise(image_array, base_variance=60),
        add_coordinate_dependent_noise(image_array, base_variance=30),
        add_coordinate_dependent_noise(image_array, base_variance=60),
    ]

    filtered_images = apply_filters(noisy_images[1])
    for index, image in enumerate(filtered_images):
        if index == 0:
            continue

        Image.fromarray(image).save(f"./images/lab-6/pigs-filtered-{index}.bmp")


    for i, noisy_image in enumerate(noisy_images):
        filtered_images = apply_filters(noisy_image)

        print("Distortion for image " + str(i))
        for j, filtered_image in enumerate(filtered_images):
            distortion = estimate_distortion(image_array, filtered_image)
            print(distortion)
        print()



if __name__ == "__main__":
    main()

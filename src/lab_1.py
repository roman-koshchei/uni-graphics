import argparse
from typing import List, Tuple
from PIL import Image
import os

# Test with all args
# python3 ./src/lab_1.py ./images/song.png ./images/town.png --new_width 500 --new_height 500 --output_dir ./images/ --old_color 237 125 67 --new_color 0 236 50 --red_balance 1.5 --green_balance 0.8 --blue_balance 1.2 --format JPEG

Color = Tuple[int, int, int]

def resize(img: Image.Image, new_width: int, new_height: int):
  return img.resize((new_width, new_height))

def is_color_match(color_a: Color, color_b: Color, tolerance: int):
  return all(abs(color_a[i] - color_b[i]) <= tolerance for i in range(3))

def change_color(img: Image.Image, old_color: Color, new_color: Color):
  data = img.getdata()

  new_data = []
  for item in data:
    if is_color_match(item, old_color, 50):
      new_data.append(new_color)
    else:
      new_data.append(item)

  img.putdata(new_data)
  return img

def balance_color(red: float = 1.0, green: float = 1.0, blue: float = 1.0):
  r, g, b = img.split()
  r = r.point(lambda i: i * red)
  g = g.point(lambda i: i * green)
  b = b.point(lambda i: i * blue)
  return Image.merge('RGB', (r, g, b))

def convert_and_save(img: Image.Image, img_path: str, output_dir: str, format: str):
  img.save(output_dir + os.path.splitext(os.path.basename(img_path))[0] + ".jpg", format)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Process images with resizing, color change, and color balance.")
  
  parser.add_argument("imgs_paths", nargs='+', help="Paths to the input images.")
  parser.add_argument("--output_dir", type=str, default="./images/", help="Directory to save processed images.")
  
  parser.add_argument("--new_width", type=int, help="New width for the image.")
  parser.add_argument("--new_height", type=int, help="New height for the image.")

  parser.add_argument("--old_color", type=int, nargs=3, help="Old color to replace (RGB format).")
  parser.add_argument("--new_color", type=int, nargs=3, help="New color to apply (RGB format).")

  parser.add_argument("--red_balance", type=float, default=1.0, help="Red color balance multiplier.")
  parser.add_argument("--green_balance", type=float, default=1.0, help="Green color balance multiplier.")
  parser.add_argument("--blue_balance", type=float, default=1.0, help="Blue color balance multiplier.")
  
  parser.add_argument("--format", type=str, choices=["PNG", "JPEG", "BMP", "TIFF"], default="JPEG", help="Output image format (choices: 'PNG', 'JPEG', 'BMP', 'TIFF').")

  args = parser.parse_args()
  
  old_color = tuple(args.old_color) if args.old_color else None
  new_color = tuple(args.new_color) if args.new_color else None
  
  for img_path in args.imgs_paths:
    img = Image.open(img_path).convert("RGB")

    if(args.new_width or args.new_height):
      new_width = args.new_width if args.new_width is not None else img.width
      new_height = args.new_height if args.new_height is not None else img.height
      img = resize(img, new_width, new_height)

    if(old_color or new_color):
      img = change_color(img, old_color, new_color)

    img = balance_color(args.red_balance, args.green_balance, args.blue_balance)
    convert_and_save(img, img_path, args.output_dir, args.format)
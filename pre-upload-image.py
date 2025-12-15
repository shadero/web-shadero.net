import argparse
import os
from PIL import Image


def convert_and_resize(input_path, quality, max_size):
    """
    Convert the image to JPG.
    """
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        return

    try:
        img = Image.open(input_path)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if max_size is not None:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

        root, _ = os.path.splitext(input_path)
        output_path = root + ".jpg"
        img.save(output_path, "JPEG", quality=quality)

        print(f"Completed: {output_path}")
        print(f"  - Quality: {quality}")
        print(f"  - Size: {img.size[0]}x{img.size[1]}")

    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Optimize images for upload (resize & convert to JPG)"
    )

    parser.add_argument("input_file", help="Image file to process")
    parser.add_argument(
        "-q", "--quality", type=int, default=90, help="JPG quality (default: 90)"
    )
    parser.add_argument(
        "-s",
        "--max-size",
        type=str,
        default=None,
        help="Maximum size (WIDTHxHEIGHT, e.g., 1980x1080). If not specified, no resizing is performed.",
    )

    args = parser.parse_args()
    max_size = None
    if args.max_size:
        try:
            width, height = map(int, args.max_size.split("x"))
            max_size = (width, height)
        except ValueError:
            print(
                "Error: max-size must be specified in 'WIDTHxHEIGHT' format (e.g., 1980x1080)"
            )
            return

    convert_and_resize(args.input_file, args.quality, max_size)


if __name__ == "__main__":
    main()

import argparse
import os
from PIL import Image


def convert_and_resize(input_path, quality, max_size):
    """
    画像をRGBに変換し、最大サイズにリサイズしてJPG保存します。
    """
    if not os.path.exists(input_path):
        print(f"エラー: ファイル '{input_path}' が見つかりません。")
        return

    try:
        img = Image.open(input_path)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        root, _ = os.path.splitext(input_path)
        output_path = root + ".jpg"
        img.save(output_path, "JPEG", quality=quality)

        print(f"処理完了: {output_path}")
        print(f"  - 画質: {quality}")
        print(f"  - サイズ: {img.size[0]}x{img.size[1]}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="画像をアップロード用に最適化(リサイズ&JPG変換)するスクリプト"
    )

    parser.add_argument("input_file", help="処理する画像ファイル")
    parser.add_argument(
        "-q", "--quality", type=int, default=85, help="JPG品質 (デフォルト: 85)"
    )
    parser.add_argument(
        "-s",
        "--max-size",
        type=str,
        default="1980x1080",
        help="最大サイズ (幅x高さ、デフォルト: 1980x1080)",
    )

    args = parser.parse_args()

    try:
        width, height = map(int, args.max_size.split("x"))
        max_size = (width, height)
    except ValueError:
        print(
            "エラー: max-size は 'WIDTHxHEIGHT' の形式で指定してください (例: 1980x1080)"
        )
        return

    convert_and_resize(args.input_file, args.quality, max_size)


if __name__ == "__main__":
    main()

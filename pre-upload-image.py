import argparse
import os
from PIL import Image

# 設定：最大サイズ (幅, 高さ)
# 指定通り 1980x1080 に設定しています
MAX_SIZE = (1980, 1080)


def convert_and_resize(input_path, quality):
    """
    画像をRGBに変換し、最大サイズにリサイズしてJPG保存します。
    """
    if not os.path.exists(input_path):
        print(f"エラー: ファイル '{input_path}' が見つかりません。")
        return

    try:
        img = Image.open(input_path)

        # 1. アルファチャンネル(透過)対策: RGBモードへ変換
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # 2. リサイズ処理: アスペクト比維持で MAX_SIZE に収める
        # Image.Resampling.LANCZOS は高品質な縮小アルゴリズムです
        img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)

        # 出力パス作成
        root, _ = os.path.splitext(input_path)
        output_path = root + ".jpg"

        # 3. 保存
        img.save(output_path, "JPEG", quality=quality)

        # 結果表示 (変換後のサイズも表示)
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

    args = parser.parse_args()

    convert_and_resize(args.input_file, args.quality)


if __name__ == "__main__":
    main()

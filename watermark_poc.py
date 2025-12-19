import cv2
import numpy as np
from imwatermark import WatermarkDecoder, WatermarkEncoder


def main() -> None:
    watermark_text = "MySecret123"
    watermark_bytes = watermark_text.encode("ascii")
    origin_path = "origin_test.jpg"
    signed_path = "output_signed.png"

    np.random.seed(42)
    near_white_image = np.random.randint(200, 256, (512, 512, 3), dtype=np.uint8)
    cv2.imwrite(origin_path, near_white_image)
    print("原图已生成")

    encoder = WatermarkEncoder()
    encoder.set_watermark("bytes", watermark_bytes)
    watermark_bit_length = encoder.get_length()
    original = cv2.imread(origin_path)
    encoded = encoder.encode(original, "dwtDct")
    encoded_uint8 = np.clip(np.round(encoded), 0, 255).astype(np.uint8)
    cv2.imwrite(signed_path, encoded_uint8)
    print("水印嵌入完成")

    reloaded = cv2.imread(signed_path)
    decoder = WatermarkDecoder("bytes", watermark_bit_length)
    extracted = decoder.decode(reloaded, "dwtDct")
    if isinstance(extracted, bytes):
        decoded_text = extracted.decode("ascii", errors="ignore")
    else:
        decoded_text = extracted.tobytes().decode("ascii", errors="ignore")
    print(f"检测到的水印内容: {decoded_text}")


if __name__ == "__main__":
    main()

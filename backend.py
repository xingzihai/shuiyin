import cv2
import numpy as np
from imwatermark import WatermarkDecoder, WatermarkEncoder


class WatermarkEngine:
    def __init__(self) -> None:
        self.algorithm = "dwtDctSvd"
        self.watermark_len = 64

    def embed(self, input_path: str, text: str, output_path: str) -> None:
        bgr = cv2.imread(input_path, cv2.IMREAD_COLOR)
        if bgr is None:
            raise ValueError("无法读取图片")

        byte_data = text.encode("utf-8")
        if len(byte_data) > 8:
            byte_data = byte_data[:8]
        else:
            byte_data = byte_data + b"\x00" * (8 - len(byte_data))

        encoder = WatermarkEncoder()
        encoder.set_watermark("bytes", byte_data)
        encoded = encoder.encode(bgr, self.algorithm, scales=[36, 36, 0])
        encoded_uint8 = np.clip(np.round(encoded), 0, 255).astype(np.uint8)
        if not cv2.imwrite(output_path, encoded_uint8):
            raise RuntimeError("保存输出图片失败")

    def extract(self, target_path: str) -> str:
        bgr = cv2.imread(target_path, cv2.IMREAD_COLOR)
        if bgr is None:
            return "Error: 无法读取图片"

        decoder = WatermarkDecoder("bytes", length=self.watermark_len)
        watermark = decoder.decode(bgr, self.algorithm, scales=[36, 36, 0])

        if isinstance(watermark, bytes):
            raw_bytes = watermark
        else:
            raw_bytes = watermark.tobytes()

        decoded_text = raw_bytes.rstrip(b"\x00").decode("utf-8", errors="ignore")
        filtered = "".join(ch for ch in decoded_text if 32 <= ord(ch) <= 126)
        return filtered


if __name__ == "__main__":
    engine = WatermarkEngine()
    dummy = np.ones((512, 512, 3), dtype=np.uint8) * 255
    cv2.imwrite("test_origin.jpg", dummy)

    print("开始嵌入...")
    engine.embed("test_origin.jpg", "TEST", "test_out.png")
    print("开始提取...")
    res = engine.extract("test_out.png")
    print(f"最终结果: {res}")

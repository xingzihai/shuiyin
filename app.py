import os
import cv2
import numpy as np
import streamlit as st
from backend import WatermarkEngine


engine = WatermarkEngine()

st.set_page_config(page_title="隐形水印工具 (Invisible Watermark)", page_icon="💧")
st.title("隐形水印工具 (Invisible Watermark)")

mode = st.sidebar.radio(
    "选择功能",
    ("🔒 添加水印 (Encrypt)", "🔓 解密水印 (Decrypt)"),
)


def save_upload(file_obj, path: str) -> None:
    with open(path, "wb") as f:
        f.write(file_obj.read())


if mode.startswith("🔒"):
    st.header("添加水印 (Encrypt)")
    uploaded = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    text = st.text_input("Watermark Text", value="MyCopyright")

    if st.button("生成"):
        if not uploaded:
            st.warning("请先上传图片。")
        else:
            temp_input = "temp_input.jpg"
            temp_output = "temp_output.png"
            save_upload(uploaded, temp_input)
            try:
                engine.embed(temp_input, text, temp_output)
                st.success("水印生成完成。")
                st.image(temp_output, caption="已添加水印的图片")
                with open(temp_output, "rb") as f:
                    st.download_button(
                        "下载水印图片",
                        f,
                        file_name="watermarked.png",
                        mime="image/png",
                    )
            except Exception as exc:
                st.error(f"处理失败: {exc}")

elif mode.startswith("🔓"):
    st.header("解密水印 (Decrypt)")
    uploaded = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if st.button("解密"):
        if not uploaded:
            st.warning("请先上传待解密的图片。")
        else:
            temp_check = "temp_check.png"
            save_upload(uploaded, temp_check)
            try:
                result = engine.extract(temp_check)
                st.success(f"提取结果: {result}")
            except Exception as exc:
                st.error(f"解密失败: {exc}")

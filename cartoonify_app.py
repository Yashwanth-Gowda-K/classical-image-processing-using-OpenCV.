import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.title("Cartoon your image")
uploaded_file = st.file_uploader("upload an Image", type=['jpg','png','jpeg'])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)

    img = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.medianBlur(gray, 5)

    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY,
                                  9,9)

    color = cv2.bilateralFilter(img, 9, 300,300)

    cartoon = cv2.bitwise_and(color, color, mask=edges)

    st.image([img, cartoon], caption=['orginial', 'cartoon'], width=300)

    cartoon_pil = Image.fromarray(cartoon)
    buf = io.BytesIO()
    cartoon_pil.save(buf, format='PNG')
    byte_im = buf.getvalue()

    st.download_button(
        label="Download",
        data=byte_im,
        file_name="Cartoonified.png",
        mime="image/png"
    )
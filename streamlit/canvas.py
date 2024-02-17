import streamlit as st
import numpy as np
from PIL import Image, ImageDraw

# Kích thước của vùng vẽ
canvas_size = (400, 400)

# Tạo một hình ảnh trống
image = Image.new("RGB", canvas_size, "white")
draw = ImageDraw.Draw(image)

# Vẽ bounding box trên canvas
def draw_bounding_box(draw, bbox, color=(255, 0, 0), width=2):
    draw.rectangle(bbox, outline=color, width=width)

# Hiển thị canvas và chức năng vẽ bounding box
st.title("Bounding Box Drawing")

canvas = st.image(image, caption='Canvas', width=canvas_size[0])

# Bắt đầu vẽ bounding box khi nút được nhấn
drawing = st.checkbox("Start Drawing Bounding Box")

if drawing:
    st.write("Click and drag to draw the bounding box.")
    start_point = None
    end_point = None
    while drawing:
        # Lấy tọa độ chuột
        xy = st.beta_columns(2)
        with xy[0]:
            x = st.slider("X", min_value=0, max_value=canvas_size[0] - 1)
        with xy[1]:
            y = st.slider("Y", min_value=0, max_value=canvas_size[1] - 1)

        current_point = (x, y)

        if st.button("Set Start Point"):
            start_point = current_point
        elif st.button("Set End Point"):
            end_point = current_point

        if start_point is not None and end_point is not None:
            bbox = [start_point, end_point]
            draw_bounding_box(draw, bbox)
            canvas.image(image)
            start_point = None
            end_point = None

        # Kiểm tra xem người dùng đã kết thúc vẽ bounding box chưa
        drawing = st.checkbox("Continue Drawing Bounding Box")

st.write("Bounding box drawing finished.")

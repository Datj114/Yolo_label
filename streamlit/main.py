import streamlit as st
import os
from streamlit_option_menu import option_menu
import numpy as np
from PIL import Image, ImageDraw
import cv2 
st.title("Dán nhãn Yolo")
session_state = st.session_state
col1_a , col2_a= st.columns(2)
# from tkinter import Tk, simpledialog
import pandas as pd 
def upload_image():
    uploaded_file = None 
    image_source = st.sidebar.radio('Chọn nguồn ảnh', ['Webcam', 'Chọn ảnh từ máy'])
    if image_source == 'Webcam':
        uploaded_file = st.camera_input('Chụp ảnh từ webcam')
    else:
        uploaded_file = st.sidebar.file_uploader("Chọn ảnh...", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        return [uploaded_file]


def upload_folder():
    folder_path = st.text_input("Enter folder path:")
    
    if folder_path and os.path.exists(folder_path):
        image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)
                       if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        return image_files
    else:
        st.warning("Please enter a valid folder path.")
        return None


# df = pd.DataFrame(columns=["Image", "Index", "X", "Y", "Width", "Height"])

    # Khởi tạo biến toàn cục

def draw_rectangle(event, x, y, flags, param):
    global index
    img = (
        param["img"],
    )
    global top_left_pt, bottom_right_pt, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        top_left_pt = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bottom_right_pt = (x, y)
        # Vẽ bounding box và văn bản lên ảnh
        cv2.rectangle(img, top_left_pt, bottom_right_pt, (0, 255, 0), 2)
        # text = simpledialog.askstring("Nhập văn bản", "Nhập nội dung:")
        #
        # cv2.putText(img, text, top_left_pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Hiển thị ảnh với bounding box và văn bản
        cv2.imshow('Image with Bounding Box', img)

        # Lưu thông tin bounding box và văn bản vào một tệp văn bản



def save_info(image, index, top_left_pt, bottom_right_pt):
        # Lưu thông tin bounding box vào DataFrame
        global df
        df = df.append({"Image": image, "Index": index, "X": top_left_pt[0], "Y": top_left_pt[1], "Width": bottom_right_pt[0] - top_left_pt[0], "Height": bottom_right_pt[1] - top_left_pt[1]}, ignore_index=True)
        return df 

       
    
def Tools_():
    images_uploaded = session_state.images_uploaded
    if images_uploaded is None:
        st.warning("Please upload an image first!")
        return 
    selected = st.selectbox("Main Menu", ["Create RectBox", "Delete RectBox",'Zoom in', "Zoom out"])
    if selected == "Create RectBox":
        if images_uploaded:
            index = 0 
            for image in images_uploaded:
                st.image(image)
                if st.button(f"Draw Bounding Box {index}"):
                    img = image 
                    img_copy = img
                    # Khởi tạo biến toàn cục
                    drawing = False
                    top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)

                    param = {"img": img}
                    cv2.namedWindow("Image with Bounding Box")
                    cv2.setMouseCallback("Image with Bounding Box", draw_rectangle, param)

                    while True:
                        cv2.imshow("Image with Bounding Box", img)
                        # Ấn phím 'esc' để thoát
                        key = cv2.waitKey(1) & 0xFF
                        if key == 27:
                            break

                    cv2.destroyAllWindows()
        else:
            st.write("No images uploaded yet!")


def action():
    # # Chọn ảnh từ máy tính
    # st.sidebar.header('st.button')

    # if st.sidebar.button('Open'):
    #    
    # if st.sidebar.button('Sliner'):
    #     st.subheader('Range slider')

    #     values = st.slider(
    #         'Select a range of values',
    #         0.0, 100.0, (25.0, 75.0))
    #     st.write('Values:', values)
    # if st.sidebar.button('line_chart'):
    #     import pandas as pd
    #     import numpy as np

    #     st.header('Line chart')

    #     chart_data = pd.DataFrame(
    #         np.random.randn(20, 3),
    #         columns=['a', 'b', 'c'])

    #     st.line_chart(chart_data)
    # if st.sidebar.button('selectbox'):
    #     option = st.selectbox(
    #         'What is your favorite color?',
    #         ('Blue', 'Red', 'Green'))

    #     if option == 'Blue':
    #         st.write("My favorite color is blue")
    # if st.sidebar.button('multiselect'):
    #     options = st.multiselect(
    #          'What are your favorite colors',
    #          ['Green', 'Yellow', 'Red', 'Blue'],
    #          ['Yellow', 'Red'])
    #     st.write('You selected:', options)
    # if st.sidebar.button('checkbox'):
    #     st.title('st.checkbox')

    #     st.write ('What would you like to order?')
    #     icecream = st.checkbox('Ice cream')
    #     coffee = st.checkbox('Coffee')
    #     cola = st.checkbox('Cola')

    #     if icecream:
    #         st.write("Great! Here's some more 🍦")

    #     if coffee:
    #         st.write("Okay, here's some coffee ☕")

    #     if cola:
    #         st.write("Here you go 🥤")
    # import streamlit as st



    # 1. as sidebar menu
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", "Open",'Open dir', "Tools",'Settings','Save'], 
            icons=['house', 'cloud-upload','folder',"list-task", 'gear','folder'], menu_icon="cast", default_index=1)
        selected
        if selected == "Open":
            images_uploaded = upload_image()
            if images_uploaded:
                for image in images_uploaded:
                    with col1_a :
                        st.image(image, caption='Uploaded Image', use_column_width=True)

        elif selected == "Open dir": 
            images_uploaded = upload_folder()
            if images_uploaded:
                for image in images_uploaded:
                    with col1_a:
                        st.image(image, caption='Uploaded Image', use_column_width=True)
        elif selected == "Tools":
            Tools_()

action()
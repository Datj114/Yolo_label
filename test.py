import streamlit as st
import os
import cv2
from tkinter import Tk, simpledialog
import shutil
from zipfile import ZipFile
from streamlit_option_menu import option_menu
import numpy as np
from PIL import Image, ImageDraw

st.title("Dán nhãn Yolo")
session_state = st.session_state
col1_a, col2_a = st.columns(2)
# from tkinter import Tk, simpledialog
import pandas as pd

# Tạo thư mục mới trong thư mục hiện tại
destination_folder = os.path.join(os.getcwd(), "uploaded_images")
# os.getcwd() giúp lấy địa chỉ path hiện tại
os.makedirs(destination_folder, exist_ok=True)


# os.makedirs(destination_folder, exist_ok=True) được sử dụng để tạo thư mục mới.
def upload_image():
    uploaded_file = None
    image_source = st.radio("Chọn nguồn ảnh", ["Webcam", "Chọn ảnh từ máy"])
    if image_source == "Webcam":
        uploaded_file = st.camera_input("Chụp ảnh từ webcam")
        file_path = os.path.join(destination_folder, "webcam_image.jpg")
    else:
        uploaded_file = st.file_uploader(
            "Chọn ảnh...",
            type=[
                "jpg",
                "png",
                "jpeg",
            ],
        )
        file_path = os.path.join(destination_folder, "image.jpg")
    if uploaded_file is not None:
        # Tạo đường dẫn cho tệp tin mới

        # Ghi dữ liệu hình ảnh vào tệp tin
        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())
        return [uploaded_file]


def upload_folder():
    folder_path = st.text_input("Enter folder path:")

    if folder_path and os.path.exists(folder_path):
        image_files = [
            os.path.join(folder_path, filename)
            for filename in os.listdir(folder_path)
            for filename in os.listdir(folder_path)
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        # for image in image_files:
        #     # Đọc dữ liệu từ tệp gốc
        #     with open(os.path.join(folder_path, image), "rb") as file:
        #         image_data = file.read()

        #     # Ghi dữ liệu vào tệp mới
        #     with open(os.path.join(destination_folder, image), "wb") as new_file:
        #         new_file.write(image_data)
        for image_path in image_files:
            # Tạo đường dẫn mới cho tệp ảnh trong thư mục đích
            new_image_path = os.path.join(
                destination_folder, os.path.basename(image_path)
            )
            # Di chuyển tệp ảnh
            shutil.move(image_path, new_image_path)
            return image_files
    else:
        st.warning("Please enter a valid folder path.")
        return None


# df = pd.DataFrame(columns=["Image", "Index", "X", "Y", "Width", "Height"])

# Khởi tạo biến toàn cục


# def draw_rectangle(event, x, y, flags, param):
#     global index
#     img = (param["img"],)
#     global top_left_pt, bottom_right_pt, drawing
#     if event == cv2.EVENT_LBUTTONDOWN:
#         drawing = True
#         top_left_pt = (x, y)

#     elif event == cv2.EVENT_LBUTTONUP:
#         drawing = False
#         bottom_right_pt = (x, y)
#         # Vẽ bounding box và văn bản lên ảnh
#         cv2.rectangle(img, top_left_pt, bottom_right_pt, (0, 255, 0), 2)
#         # text = simpledialog.askstring("Nhập văn bản", "Nhập nội dung:")
#         #
#         # cv2.putText(img, text, top_left_pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#         # Hiển thị ảnh với bounding box và văn bản
#         cv2.imshow("Image with Bounding Box", img)

#         # Lưu thông tin bounding box và văn bản vào một tệp văn bản


# def save_info(image, index, top_left_pt, bottom_right_pt):
#     # Lưu thông tin bounding box vào DataFrame
#     global df
#     df = df.append(
#         {
#             "Image": image,
#             "Index": index,
#             "X": top_left_pt[0],
#             "Y": top_left_pt[1],
#             "Width": bottom_right_pt[0] - top_left_pt[0],
#             "Height": bottom_right_pt[1] - top_left_pt[1],
#         },
#         ignore_index=True,
#     )
#     return df


# Tạo tệp tin tên data_name.txt trong một thư mục được chỉ định
def create_data_name_file(dictionary, folder_path):
    file_path = os.path.join(folder_path, "data_name.txt")  # nối tệp vs thư mục
    with open(
        file_path, "w"
    ) as data_name_file:  # Lặp qua từng cặp chỉ mục - nhãn trong từ điển, ghi thông tin này vào tệp tin "data_name.txt".
        for index, label in dictionary.items():
            data_name_file.write(f"{label} {index} \n")


# Tạo một đường dẫn đầy đủ đến tệp tin văn bản liên quan đến tệp ảnh
def file_in_folder_path(folder_path, image_path):
    return os.path.join(
        folder_path, f"{os.path.splitext(os.path.basename(image_path))[0]}.txt"
    )


def create_label_files(
    file_in_folder_path, index, x_candidate, y_candidate, width, hight
):
    with open(file_in_folder_path, "a") as label_file:
        label_file.write(
            f"{str(index)} {str(x_candidate)} {str(y_candidate)} {str(width)} {str(hight)}\n"
        )


def draw_and_save(event, x, y, flags, param):

    global index
    text_file_path, dictionary, img = (
        param["text_file_path"],
        param["dictionary"],
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
        cv2.imshow("Image with Bounding Box", img)

        text = simpledialog.askstring("Nhập tên", "Nhập tên cho bounding box:")

        if text is not None:
            if text not in dictionary:
                index = index + 1
                dictionary[text] = index

            create_label_files(
                text_file_path,
                dictionary.get(text),
                top_left_pt[0],
                top_left_pt[1],
                abs(bottom_right_pt[0] - top_left_pt[0]),
                abs(bottom_right_pt[1] - top_left_pt[1]),
            )

            cv2.putText(
                img,
                f"{text}",
                top_left_pt,
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
            # Hiển thị ảnh với bounding box và văn bản
            cv2.imshow("Image with Bounding Box", img)


def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)


def move_folder_and_file_to_new_folder(source_folder, source_file, destination_folder):
    shutil.move(
        source_file, os.path.join(destination_folder, os.path.basename(source_file))
    )
    shutil.move(source_folder, destination_folder)


# Hàm zip_folder được thiết kế để nén một thư mục và tạo một tệp tin nén (zip file)
def zip_folder(zip_file_path):
    shutil.make_archive(zip_file_path, "zip", zip_file_path)


# Tạo thư mục mới trong thư mục hiện tại
folder_Yolo = os.path.join(os.getcwd(), "folder_Yolo")
index = -1


def Tools_():
    # khởi tạo biến index
    dictionary = (
        dict()
    )  # Khởi tạo một từ điển trống để lưu trữ tên và chỉ mục của bounding box
    # Tạo thư mục mới trong thư mục hiện tại

    folder_Yolo = os.path.join(os.getcwd(), "folder_Yolo")
    create_folder(
        folder_Yolo
    )  # tạo thư mục chính. Hàm này sẽ tạo thư mục nếu nó chưa tồn tại.
    folder_in_new_folder_path = os.path.join(folder_Yolo, "folder_")
    create_folder(
        folder_in_new_folder_path
    )  # để tạo thư mục con bên trong thư mục chính. Nếu nó chưa tồn tại, thì sẽ được tạo mới.
    image_files = [
        file
        for file in os.listdir(destination_folder)
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    ]

    for image_file in image_files:
        image_path = os.path.join(destination_folder, image_file)
        text_file_path = file_in_folder_path(folder_in_new_folder_path, image_path)
        img = cv2.imread(image_path)
        img_copy = img.copy()
        # Khởi tạo biến toàn cục
        drawing = False
        top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)

        param = {"text_file_path": text_file_path, "dictionary": dictionary, "img": img}
        cv2.namedWindow("Image with Bounding Box")
        cv2.setMouseCallback("Image with Bounding Box", draw_and_save, param)

        while True:
            cv2.imshow("Image with Bounding Box", img)
            # Ấn phím 'esc' để thoát
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break

        cv2.destroyAllWindows()

    create_data_name_file(dictionary, folder_Yolo)


def Add():
    zip_folder(folder_Yolo)


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
        selected = option_menu(
            "Main Menu",
            ["Home", "Open", "Open dir", "Label", "Add to zip"],
            icons=["house", "cloud-upload", "folder", "list-task", "folder"],
            menu_icon="cast",
            default_index=1,
        )

        selected
        if selected == "Open":
            with col1_a:
                images_uploaded = upload_image()
            if images_uploaded:
                for image in images_uploaded:
                    with col2_a:
                        st.image(image, caption="Uploaded Image", use_column_width=True)

        elif selected == "Open dir":
            with col1_a:
                images_uploaded = upload_folder()
            if images_uploaded:
                for image in images_uploaded:
                    with col2_a:
                        st.image(image, caption="Uploaded Image", use_column_width=True)
        elif selected == "Label":
            Tools_()
        elif selected == "Add to zip":
            Add()


action()

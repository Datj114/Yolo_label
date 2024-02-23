import streamlit as st
import os
import cv2
from tkinter import Tk , simpledialog
import shutil
from zipfile import ZipFile
from streamlit_option_menu import option_menu
from PIL import Image, ImageDraw
st.title("Dán nhãn Yolo")
session_state = st.session_state
col1_a, col2_a = st.columns(2)


# Tạo thư mục mới trong thư mục hiện tại
destination_folder = os.path.join(os.getcwd(), "uploaded_images")


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
        # Ghi dữ liệu hình ảnh vào tệp tin
        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())
        return uploaded_file
        

def upload_folder():
    folder_path = st.text_input("Enter folder path:")

    if folder_path and os.path.exists(folder_path):
        image_files = [
            os.path.join(folder_path, filename)
            for filename in os.listdir(folder_path)
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        return image_files
    else:
        st.warning("Please enter a valid folder path.")
        return None


# Tạo tệp tin tên data_name.txt trong một thư mục được chỉ định
def create_data_name_file(dictionary, folder_path):
    file_path = os.path.join(folder_path, "data_name.txt")  # nối tệp vs thư mục
    with open(
        file_path, "a"
    ) as data_name_file:  # Lặp qua từng cặp chỉ mục - nhãn trong từ điển, ghi thông tin này vào tệp tin "data_name.txt".
        for index, label in dictionary.items():
            data_name_file.write(f"{label} {index} \n")


# Tạo một đường dẫn đầy đủ đến tệp tin văn bản liên quan đến tệp ảnh
def file_in_folder_path(folder_path, image_path):
    return os.path.join(
        folder_path, f"{os.path.splitext(os.path.basename(image_path))[0]}.txt"
    )


def create_label_files(
    file_in_folder_path, index, label_index, x_candidate, y_candidate, width, hight
):
    with open(file_in_folder_path, "a") as label_file:
        label_file.write(
            f"{str(index)} {str(label_index)} {str(x_candidate)} {str(y_candidate)} {str(width)} {str(hight)}\n"
        )


def draw_and_save(event, x, y, flags, param):

    global index
    text_file_path, dictionary, diction_label, img = (
        param["text_file_path"],
        param["dictionary"],
        param["diction_label"],
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

            index_label = 0
            if text not in diction_label:
                index_label = 0
            elif text in diction_label:
                index_label += 1
            diction_label[text] = index_label
            label_index = f"{str(text)}{str(diction_label[text])}"
            create_label_files(
                text_file_path,
                dictionary.get(text),
                label_index,
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

# Hàm zip_folder được thiết kế để nén một thư mục và tạo một tệp tin nén (zip file)
def zip_folder(zip_file_path):
    shutil.make_archive(zip_file_path, "zip", zip_file_path)


# Tạo thư mục mới trong thư mục hiện tại
folder_Yolo = os.path.join(os.getcwd(), "folder_Yolo")
index = -1


def Tools_():
    dictionary = (
        dict()
    )  # Khởi tạo một từ điển trống để lưu trữ tên và chỉ mục của bounding box
    # Tạo thư mục mới trong thư mục hiện tại
    diction_label = dict()
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

        param = {
            "text_file_path": text_file_path,
            "dictionary": dictionary,
            "diction_label": diction_label,
            "img": img,
        }
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
        if selected == "Home":
            with col1_a:
                st.write("1.Open giúp mở 1 ảnh hoặc lấy ảnh tử webcame để gán nhãn")
                st.write("2.Open dir giúp mở 1 folder chứa các ảnh để gán nhãn")
                st.write("3.Label mở chương trình gán nhãn các ảnh")
                st.write("4.Add to zip giúp tạo một file zip chứa thông tin gán nhãn")

        elif selected == "Open":
            with col1_a:
                images_uploaded = upload_image()
                print("Done", type(images_uploaded))
            if images_uploaded:
                # for image in images_uploaded:
                    with col2_a:
                        st.image(images_uploaded, caption="Uploaded Image", use_column_width=True)

        elif selected == "Open dir":
            with col1_a:
                images_uploaded = upload_folder()
            if images_uploaded:
                for image_path in images_uploaded:
                    with col1_a:
                        img = Image.open(image_path)
                        st.image(img, caption="Uploaded Image", use_column_width=True)
                        file_name = os.path.basename(image_path)
                        with open(
                            os.path.join(destination_folder, file_name), "wb"
                        ) as file:
                            img.save(file)
        elif selected == "Label":
            Tools_()
        elif selected == "Add to zip":
            Add()


action()


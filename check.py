import cv2
from tkinter import simpledialog, Tk
import os
import shutil
from zipfile import ZipFile


def create_data_name_file(dictionary, folder_path):
    file_path = os.path.join(folder_path, "data_name.txt")
    with open(file_path, "w") as data_name_file:
        for index, label in dictionary.items():
            data_name_file.write(f"{index} {label}\n")


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
            cv2.imshow("Image with Bounding Box", img)


def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)


def move_folder_and_file_to_new_folder(source_folder, source_file, destination_folder):
    shutil.move(
        source_file, os.path.join(destination_folder, os.path.basename(source_file))
    )
    shutil.move(source_folder, destination_folder)


def zip_folder(folder_path, zip_file_path):
    shutil.make_archive(zip_file_path, "zip", folder_path)


if __name__ == "__main__":
    index = 0
    dictionary = dict()
    new_folder_path = r"E:\Data_Zaloo"
    create_folder(r"E:\Data_Zaloo")
    folder_in_new_folder_path = os.path.join(new_folder_path, "folder_")
    create_folder(folder_in_new_folder_path)

    folder_path = r"C:\Users\Admin\Pictures\Screenshots"
    image_files = [
        file
        for file in os.listdir(folder_path)
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    ]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        text_file_path = file_in_folder_path(folder_in_new_folder_path, image_path)
        img = cv2.imread(image_path)
        img_copy = img.copy()

        drawing = False
        top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)

        param = {"text_file_path": text_file_path, "dictionary": dictionary, "img": img}
        cv2.namedWindow("Image with Bounding Box")
        cv2.setMouseCallback("Image with Bounding Box", draw_and_save, param)

        while True:
            cv2.imshow("Image with Bounding Box", img)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break

        cv2.destroyAllWindows()

    create_data_name_file(dictionary, new_folder_path)
    zip_folder(new_folder_path, new_folder_path)

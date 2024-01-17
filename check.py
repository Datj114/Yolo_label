# kiểm tra xem thư viện có tồn tại label chưa, nếu chưa thì thêm
def add_to_dictionary(dictionary, key, value):
    # Kiểm tra xem giá trị có trong dictionary không
    if key not in dictionary:
        # vì value là index của nhãn trước
        value = value + 1
        # Nếu không có, thêm giá trị vào dictionary
        dictionary[key] = value


# tạo 1 file ghi index và nhãn
def create_data_name_file(dictionary, folder_path):
    file_path = os.path.join(folder_path, "data_name.txt")
    with open(file_path, "a") as data_name_file:
        for index, label in dictionary.items():
            data_name_file.write(f"{index} {label}\n")


# tạo địa chỉ đến file txt trong folder
def file_in_folder_path(folder_path, image_path):
    # image_path: địa chỉ đền file ảnh
    return os.path.join(
        folder_path, f"{os.path.splitext(os.path.basename(image_path))[0]}.txt"
    )


# ghi giá trị vào file txt
def create_label_files(
    file_in_folder_path, index, x_candidate, y_candidate, width, hight
):
    # file_in_folder_path: địa chỉ đến file ghi
    with open(file_in_folder_path, "a") as label_file:
        label_file.write(
            f"{str(index)} {str(x_candidate)} {str(y_candidate)} {str(width)} {str(hight)}\n"
        )


import os
import shutil
from zipfile import ZipFile


# chuyển file và folder labels vào một folder mới
def move_folder_and_file_to_new_folder(source_folder, source_file, destination_folder):
    # Di chuyển tập tin vào thư mục đích
    shutil.move(
        source_file, os.path.join(destination_folder, os.path.basename(source_file))
    )

    # Di chuyển thư mục vào thư mục đích
    shutil.move(source_folder, destination_folder)


def zip_folder(folder_path, zip_file_path):
    # Tạo file ZIP và thêm nội dung từ thư mục
    shutil.make_archive(zip_file_path, "zip", folder_path)


def create_folder(folder_path):
    # folder_path: là đường dẫn đến thư mục sau khi tạo
    os.makedirs(folder_path, exist_ok=True)


### cần tạo một folder sau đó tạo 1 file trong đố, 1 folder trong đó
# Tạo thư mục (chỉ tạo thư mục cấp độ hiện tại)
new_folder_path = r"E:\Data_Zaloo"
create_folder(r"E:\Data_Zaloo")
# tạo file data_name.txt trong thư mục vừa tạo
dictionary = {"a": 1, "b": 2, "c": 3}
create_data_name_file(dictionary, new_folder_path)
# tạo một thư mục mới trong thư mục vừa tạo
folder_in_new_folder_path = os.path.join(new_folder_path, "folder_")
create_folder(folder_in_new_folder_path)
# Đường dẫn file .txt trong thư mục đích sau khi tạo xong
text_file_path = file_in_folder_path(
    folder_in_new_folder_path, r"E:\z4862598311456_369368c90ec692e8d439853b7084ab0a.jpg"
)
# Gọi hàm để tạo nội dung cho file .txt
create_label_files(text_file_path, 0, 10, 20, 30, 40)


#  sau đó chuyển folder vè file zip

# Gọi hàm để tạo file ZIP từ thư mục đích
zip_folder(new_folder_path, new_folder_path)

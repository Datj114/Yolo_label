# tạo địa chỉ đến file txt trong folder
def file_in_folder_path(folder_path, image_name):
    return os.path.join(folder_path, f"{os.path.splitext(image_name)[0]}.txt")


# ghi giá trị vào file txt
def create_label_files(file_in_folder_path, index, x_candidate, y_candidate, width, hight):
    # file_in_folder_path: địa chỉ đến file ghi
    with open(file_in_folder_path, "a") as label_file:
        label_file.write(
            f"{str(index)} {str(x_candidate)} {str(y_candidate)} {str(width)} {str(hight)}\n"
        )



import os
import shutil
from zipfile import ZipFile


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


# tạo địa chỉ đến file txt trong folder
def file_in_folder_path(folder_path, image_name):
    return os.path.join(folder_path, f"{os.path.splitext(image_name)[0]}.txt")


# Đường dẫn thư mục và tập tin nguồn
source_file = r"e:\Document.txt"
source_folder= r"e:\ewfolder"

# Đường dẫn thư mục đích
destination_folder = r"E:\Data_Zalo"

# Gọi hàm để di chuyển thư mục và tập tin vào thư mục đích
move_folder_and_file_to_new_folder(source_folder, source_file, destination_folder)

# Đường dẫn file .txt trong thư mục đích
text_file_path = file_in_folder_path(destination_folder, r"E:\z4862598311456_369368c90ec692e8d439853b7084ab0a.jpg")

# Gọi hàm để tạo nội dung cho file .txt
create_label_files(text_file_path, 0, 10, 20, 30, 40)

# Đường dẫn và tên của file ZIP đích
zip_file_path = r"E:\Data_Zalo"

# Gọi hàm để tạo file ZIP từ thư mục đích
zip_folder(destination_folder, zip_file_path)

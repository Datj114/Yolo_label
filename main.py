import os
import cv2
from tkinter import Tk, simpledialog
import zipfile

# tao folder de luu file
folder_path = '/Users/luongthaison/Documents/second years student /Python/Python-HIT-Private/final_project/label'
os.mkdir(folder_path)

# Khởi tạo biến toàn cục
drawing = False  # True khi đang vẽ bounding box
top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)

def draw_rectangle(event, x, y, flags, param):
    global top_left_pt, bottom_right_pt, drawing

    index = param[0]

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
        save_info(index, name, top_left_pt, bottom_right_pt, bottom_right_pt[0] - top_left_pt[0], bottom_right_pt[1] - top_left_pt[1])


def insert_string_into_path(base_path, inserted_string):
    # Kết hợp đường dẫn và chuỗi được chèn
    combined_path = os.path.join(base_path, inserted_string)

    # Chuẩn hóa đường dẫn
    normalized_path = os.path.normpath(combined_path)

    return normalized_path


def save_info(index, name, x_candidate, y_candidate, width, height):
    # Thực hiện các bước để lưu thông tin,
    inserted_string = f'{name}.txt'
    info_file_path = insert_string_into_path(folder_path, inserted_string)
    with open(info_file_path, 'a') as file:
        file.write(f"index : {index} ,x_candidate: {x_candidate}, y_candidate: {y_candidate} , width: {width} , height: {height}\n")


def import_to_zip():
    # tao 1 file zip
    zf = zipfile.ZipFile('file_image_labeled.zip', mode='w')


def get_image_files(folder_path):
    image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)
                   if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return image_files


if __name__ == "__main__":
    image_folder_path = r'/Users/luongthaison/Documents/second years student /Python/Python-HIT-Private/final_project/uploads'
    # danh sach  cac anh
    image_files = get_image_files(image_folder_path)
    image_names = [os.path.splitext(os.path.basename(file_path))[0] for file_path in image_files]
    index = 0
    for image_path, name in zip(image_files, image_names):
        root = Tk()
        root.withdraw()  # Ẩn cửa sổ chính của Tkinter

        img = cv2.imread(image_path)

        cv2.namedWindow('Image with Bounding Box')
        cv2.setMouseCallback('Image with Bounding Box', draw_rectangle, param=(index,))

        while True:
            cv2.imshow('Image with Bounding Box', img)
            # Ấn phím 'esc' để thoát
            if cv2.waitKey(1) & 0xFF == 27:
                break
        index += 1
        cv2.destroyAllWindows()

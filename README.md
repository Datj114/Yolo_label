## Giới thiệu 
Yolo_label_App là một tool chúng em xây dựng để gán nhãn cho hình ảnh .
## Cài Đặt 
Bước 1 : clone repository về máy : 
```
git clone https://github.com/Datj114/Yolo_label
```
Bước 2 : Cài các package yêu cầu : 
```
pip install -r requirement.txt
```
## Sử dụng 
  + Mở IDE
  + chọn thư mục, địa chỉ muốn clone về
  + mở terminal và gõ :
      ```
      streamlit run ....
      ```
##  chức năng chính : 
1. **Hiển thị các ảnh**:
2. **Tạo bouding box** : vẽ bouding box bằng chuột trực tiếp lên các ảnh 
3. **Gán nhãn cho dữ liệu**: nhãn ở đây sẽ do người dùng chủ động nhập 
4. **Lưu về máy file zip gồm** :
   + data_name.txt: chứa index và tên label
   + folder: label chứa các file tên_ảnh.txt (index_label, x_candidate, y_candidate, width, height)
## Yêu cầu hệ thống 
1. Python 3.x
2. Các thư viện trong file 'requirement.txt'
## Phản hồi 
Mọi người có thể nhận xét , commit hoặc sửa code cho chúng em để tối ưu thì càng tốt ạ :)) 
thông qua **Pull request** ạ .

      

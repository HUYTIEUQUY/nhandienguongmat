import face_recognition
import cv2
import numpy as np
import pickle
import xlsxwriter
import datetime
import sqlite3
#-------------------------------------------------- thao tac vs excel 
tengv= input("Teacher: " )
tenmh= input("Subject: " )
thoigian= str(datetime.datetime.now())
fileexcel= tenmh+"_"+str(datetime.date.today())+".xlsx"


out_workbook = xlsxwriter.Workbook("filediemdanh/test"+str(datetime.date.today())+".xlsx")
outsheet =out_workbook.add_worksheet()
outsheet.write("A1","Điểm danh học sinh đi học")






f=open("ref_name.pkl","rb")
ref_dictt=pickle.load(f) #đọc file và luu tên theo id vào biến ref_dictt
f.close()
f=open("ref_embed.pkl","rb")
embed_dictt=pickle.load(f) #đọc file và luu hình ảnh đã biết được mã hoá  theo id vào biến embed_dictt
f.close()

#-------------------------------------------------hàm tạo file excel -------------------------------------

def write_data_to_file(array,x):
    for i in range(len(array)):
        outsheet.write(i+1,x,ref_dictt[array[i]])

        #------------------------input------------------------------------


conn = sqlite3.connect("data.db")
with conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO diemdanh VALUES('"+tengv+"','"+tenmh+"','"+thoigian+"','"+fileexcel+"')")




known_face_encodings = []  
known_face_names = []  

for ref_id , embed_list in embed_dictt.items():
    for my_embed in embed_list:
        known_face_encodings +=[my_embed]
        known_face_names += [ref_id]

video_capture  = cv2.VideoCapture(0)
face_locations = []
face_encodings = []
face_names     = []
diemdanh       =[]
process_this_frame = True #xử lý khung
while True  :
  
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1] # Chuyển đổi hình ảnh từ màu BGR (OpenCV sử dụng) sang màu RGB (face_recognition sử dụng)
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)# tìm tất cả khuôn mặt trong khung hình hiện tại vủa video
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) #mã hoá khuôn mặt hiện tại trong khung hình của video
        face_names = []
        for face_encoding in face_encodings:
            # Xem khuôn mặt có khớt cới các khuôn mặt đã biết không
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            #Đưa ra các khoảng cách giữa các khuôn mặt và khuôn mặt đã biết
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances) #Cái nào gần hơn thì lưu vào biến best_match_index
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name)
            if name not in diemdanh:
                diemdanh.append(name)
    process_this_frame = not process_this_frame

    write_data_to_file(diemdanh,0)
    #Hiển thị kết quả
    for (top_s, right, bottom, left), name in zip(face_locations, face_names):
        top_s *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top_s), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, ref_dictt[name], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
out_workbook.close()
video_capture.release()
cv2.destroyAllWindows()
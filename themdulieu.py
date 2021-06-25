
import cv2 
import face_recognition
import pickle
import sqlite3


def insertOrUpdate(id, name):
    conn = sqlite3.connect('data.db')
    query = "select * from sinhvien where Id="+str(id)
    Cusror = conn.execute(query)

    isRecordExist = 0 #kiểm tra nếu có ID trong database rồi thì = 1 nếu chưa thì giữ =0
    for row in Cusror:
        isRecordExist = 1
    
    if(isRecordExist == 0):
        query = "insert into sinhvien(Id,Name) values("+str(id)+",'"+str(name)+"')"
    else:
        query = "update sinhvien set Name='"+str(name)+"'where Id="+str(id)   
    conn.execute(query)
    conn.commit()
    conn.close()

name=input("enter name: ")
ref_id=input("enter id: ")
insertOrUpdate(ref_id, name)

try:
    f=open("ref_name.pkl","rb")
    ref_dictt=pickle.load(f)
    f.close()
except:
    ref_dictt={}
ref_dictt[ref_id]=name
f=open("ref_name.pkl","wb")
pickle.dump(ref_dictt,f)
f.close()


try:
    f=open("ref_embed.pkl","rb")
    embed_dictt=pickle.load(f)
    f.close()
except:
    embed_dictt={}




for i in range(5):
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    while True:
       
        check, frame = webcam.read()
        cv2.imshow("Capturing", frame)
         # Thay đổi kích thước trong opencv
         #frame: màn hình là hình ảnh đầu vào
         #(0, 0), fx=0.25, fy=0.25 : kích thước mong muốn cho hình ảnh đầu
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1] # Chuyển đổi hình ảnh từ màu BGR (OpenCV sử dụng) sang màu RGB (face_recognition sử dụng)
  
        key = cv2.waitKey(1)
        if key == ord('s') : 
            face_locations = face_recognition.face_locations(rgb_small_frame)
            if face_locations != []: #nếu có khuôn mặt
                face_encoding = face_recognition.face_encodings(frame)[0] #mã hoá và lưu vào biến face_encoding
                if ref_id in embed_dictt: #Nếu id đã tồn tại thì cộng thêm hình ảnh đã mã hoá vào
                    embed_dictt[ref_id]+=[face_encoding]
                else:#Nếu chưa tồn tại thì khởi tạo với "id"="dữ liệu hình ảnh mã hoá"
                    embed_dictt[ref_id]=[face_encoding]
                webcam.release()
                cv2.waitKey(1)
                cv2.destroyAllWindows()
                break
        elif key == ord('q'):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows() # thoát khỏi camera
            break


f=open("ref_embed.pkl","wb")
pickle.dump(embed_dictt,f)
f.close()
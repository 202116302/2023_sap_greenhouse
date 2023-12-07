from picamera import PiCamera
from time import sleep
import face_recognition
import os

output_dir = 'sap'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

camera = PiCamera()

camera.start_preview()
sleep(1)
camera.capture(os.path.join(output_dir, 'unknown.jpg'))
camera.stop_preview()
print('done capture')

student_id = '202110065'
saved_img_name = [f for f in os.listdir('./sap/data') if f.startswith(student_id)]
saved_img = face_recognition.load_image_file(f'./sap/data/{saved_img_name[0]}')
saved_img_encoding = face_recognition.face_encodings(saved_img)[0]

unknown_img = face_recognition.load_image_file('./sap/unknown.jpg')
unknown_face_encoding = face_recognition.face_encodings(unknown_img)[0]

results = face_recognition.compare_faces([saved_img_encoding], unknown_face_encoding)

if results[0] == True:
    conf_name = saved_img_name[0].split('.')[0].split('_')[-1]
    print(f'{conf_name} 확인')
else:
    print('등록된 사람이 아닙니다')

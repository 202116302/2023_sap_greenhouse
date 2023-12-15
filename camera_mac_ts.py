import face_recognition
import cv2
import os
from datetime import datetime
import pandas as pd

while True:
    student_id = str(input('student ID: '))

    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    unknown_img_name = './sap/unknown.jpg'
    cv2.imwrite(unknown_img_name, frame)

    saved_img_name = [f for f in os.listdir('./sap/data') if f.startswith(student_id)]
    if not saved_img_name:
        print('등록된 사용자가 아닙니다.\n-------------------')

    else:

        saved_img = face_recognition.load_image_file(f'./sap/data/{saved_img_name[0]}')
        saved_img_encoding = face_recognition.face_encodings(saved_img)[0]

        unknown_img = face_recognition.load_image_file('./sap/unknown.jpg')
        unknown_face_encoding = face_recognition.face_encodings(unknown_img)[0]

        results = face_recognition.compare_faces([saved_img_encoding], unknown_face_encoding, tolerance=0.45)

        if results[0] == True:
            conf_name = saved_img_name[0].split('.')[0].split('_')[-1]
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{conf_name}님 안녕하세요.\n-------------------')

            df = pd.DataFrame({
                'timestamp': [str(date_time)],
                'name': [conf_name]
            })

            output_dir = './sap'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            if not os.path.isfile(os.path.join(output_dir, 'manage.csv')):
                df.to_csv(os.path.join(output_dir, 'manage.csv'), encoding='utf-8-sig', index=False)
            else:
                df_origin = pd.read_csv(os.path.join(output_dir, 'manage.csv'))
                df_save = pd.concat([df_origin, df])
                df_save.to_csv(os.path.join(output_dir, 'manage.csv'), encoding='utf-8-sig', index=False)

        else:
            print('사용자를 찾을 수 없습니다.\n-------------------')

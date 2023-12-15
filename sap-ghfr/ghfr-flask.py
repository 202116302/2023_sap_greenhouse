from flask import Flask, render_template, request
import face_recognition
from datetime import datetime
import pandas as pd
import os
from picamera import PiCamera
import time

app = Flask(__name__)

@app.route('/')
def home():
    current_date = datetime.now().strftime('%Y.%m.%d')
    return render_template('index.html', current_date=current_date)

@app.route('/', methods=['POST'])
def recognize_face():
    student_id = request.form['student_id']

    saved_img_name = [f for f in os.listdir('../../../../Downloads/ghfr/data') if f.startswith(student_id)]

    if not saved_img_name:
        return render_template('index.html', error_message='등록된 사용자가 아닙니다.')

    camera = PiCamera()
    camera.start_preview()
    time.sleep(2)
    camera.capture('./unknown.jpg')
    camera.stop_preview()
    camera.close()

    saved_img = face_recognition.load_image_file(f'./data/{saved_img_name[0]}')
    saved_img_encoding = face_recognition.face_encodings(saved_img)[0]

    unknown_img = face_recognition.load_image_file('./unknown.jpg')
    unknown_face_encoding = face_recognition.face_encodings(unknown_img)
    
    if len(unknown_face_encoding) >= 1:
        unknown_face_encoding = unknown_face_encoding[0]

        results = face_recognition.compare_faces([saved_img_encoding], unknown_face_encoding, tolerance=0.45)

        if results[0]:
            conf_name = saved_img_name[0].split('.')[0].split('_')[-1]
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            df = pd.DataFrame({
                'timestamp': [str(date_time)],
                'name': [conf_name]
            })

            output_dir = '../../../../Downloads/ghfr/result'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            if not os.path.isfile(os.path.join(output_dir, 'manage.csv')):
                df.to_csv(os.path.join(output_dir, 'manage.csv'), encoding='utf-8-sig', index=False)
            else:
                df_origin = pd.read_csv(os.path.join(output_dir, 'manage.csv'))
                df_save = pd.concat([df_origin, df])
                df_save.to_csv(os.path.join(output_dir, 'manage.csv'), encoding='utf-8-sig', index=False)

            return render_template('index.html', success_message=f'{conf_name}님 안녕하세요.', conf_name=conf_name)
        else:
            return render_template('index.html', warning_message='사용자와 일치하지 않습니다.')
    else:
        return render_template('index.html', warning_message='사용자와 일치하지 않습니다.')

if __name__ == '__main__':
    app.run(debug=True)

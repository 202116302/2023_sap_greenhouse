from flask import Flask, render_template, request, redirect, url_for
import face_recognition
import os
from PIL import Image

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compare_faces', methods=['POST'])
def compare_faces():
    student_id = request.form['student_id']

    saved_img_name = [f for f in os.listdir('./data') if f.startswith(student_id)]

    if len(saved_img_name) < 1:
        results = '등록된 사용자가 아닙니다.'
    else:
        user_uploaded_file = request.files['camera']
        user_uploaded_image = Image.open(user_uploaded_file)
        rotated_image = user_uploaded_image.rotate(-90)
        rotated_image.save('user.jpg')

        saved_img = face_recognition.load_image_file(f'./data/{saved_img_name[0]}')
        saved_img_encoding = face_recognition.face_encodings(saved_img)[0]

        unknown_img = face_recognition.load_image_file('user.jpg')
        unknown_face_encoding = face_recognition.face_encodings(unknown_img)

        if len(unknown_face_encoding) >= 1:
            unknown_face_encoding = unknown_face_encoding[0]

            results = face_recognition.compare_faces([saved_img_encoding], unknown_face_encoding, tolerance=0.55)

            if results[0]:
                results = saved_img_name[0].split('.')[0].split('_')[-1]

                return render_template('dashboard.html', results=results)
        else:
            results = '등록된 사용자와 일치하지않습니다.'

    return render_template('index.html', results=results)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)